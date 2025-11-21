import re
import unicodedata
from typing import List, Dict, Any, Optional, Iterable
from config.settings import FUZZY_LOGIC_ACCURACY_GENERAL_RAG
from .llm_patterns import (COURTESY_RE, NEXOS_RE, SPLIT_RE, INTENT_RES, INTENT_PRIORITY, INTENT_ROUTING)

def norm_text(s: str, courtesy_flag: bool) -> str:
    """ Normalize text for matching:
    - lowercase
    - remove accents
    - remove punctuation (keep spaces)
    - remove courtesy words (por favor, gracias, etc)
    - collapse multiple spaces"""

    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode("ascii")
    s = re.sub(r'[^a-z0-9 ]+',' ', s.lower())
    if courtesy_flag:
        s = COURTESY_RE.sub(' ', s)
    return re.sub(r'\s+',' ', s).strip()

def best_hit(res) -> Dict[str, Any]:
    """ From the result of general_rag.lookup (dict or list of dicts), return the best one (highest score)"""
    if isinstance(res, list) and res:
        return max((x for x in res if isinstance(x, dict)), key=lambda x: x.get('score', 0.0), default={})
    return res if isinstance(res, dict) else {}

def detect_intent(t: str, order: Optional[Iterable[str]] = None, normalizer=None) -> Optional[str]:
    """ From a text, detect the intent by matching regexes in order.
    If 'order' is given, use that order (otherwise use INTENT_PRIORITY).
    If 'normalizer' is given, use it to normalize the text before matching (otherwise use norm_text).
    Return the name of the first matching intent, or None if no match. """
    nt = normalizer(t, True) if normalizer else t
    for name in (order or INTENT_PRIORITY):
        rex = INTENT_RES.get(name)
        if rex and rex.search(nt):
            return name
    return None

def split_and_prioritize(text: str, general_rag) -> List[Dict[str, Any]]:
    """
    From a text, split it into clauses (by connectors) and classify each clause.
    Since navigation is removed, this will mostly route to 'general' or 'rag'.
    """
    t = norm_text(text, True)

    parts = SPLIT_RE.split(t)
    clauses = [p.strip() for p in parts if p and not NEXOS_RE.fullmatch(p.strip())]

    if not clauses:
        clauses.append(norm_text(text, False))

    accions = []
    for c in clauses:
        print(c, flush=True)
        # 1) Respuestas cortas por GENERAL_RAG si hay alta confianza
        var = best_hit(general_rag.lookup(c))
        if var.get('answer') and var.get('score', 0.0) >= FUZZY_LOGIC_ACCURACY_GENERAL_RAG:
            accions.append(("first", "rag", {"data": var['answer'].strip()}))
            continue
        intent = detect_intent(c, order=INTENT_PRIORITY, normalizer=norm_text)
        spec = INTENT_ROUTING.get(intent)

        if spec:
            params = {"data": c} if spec.get("need_user_input") else {}
            accions.append((spec["kind_group"], spec["kind"], params))
        else:
            accions.append(("second", "general", {"data": c}))

    # Primero cortas, luego largas (orden estable preservado)
    print(clauses, flush=True)
    print(accions, flush=True)
    accions.sort(key=lambda x: 0 if x[0] == "first" else 1)
    return [{"kind": k, "params": p} for _, k, p in accions]