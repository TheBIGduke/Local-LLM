import json
from typing import List, Dict, Any
from difflib import SequenceMatcher
from rapidfuzz import fuzz as rf_fuzz
HAS_RF = True

from config.settings import FUZZY_LOGIC_ACCURACY_GENERAL_RAG
from llm.llm_intentions import norm_text

class GENERAL_RAG:
    def __init__(self, path: str):
        self.items: List[Dict[str,str]] = []
        self.load(path)
    
    def load(self, path: str) -> None:
        """ Load the GENERAL_RAG from a JSON file or line-separated JSON objects """
        print("[llm_data] Cargando GENERAL_RAG", flush=True)
        try:
            with open(path, "r", encoding="utf-8") as f:
                txt = f.read().strip()

            try:
                obj = json.loads(txt)
                items: List[Dict[str,str]] = []
                
                if isinstance(obj, dict):
                    for _, lst in obj.items():
                        if isinstance(lst, list):
                            for it in lst:
                                ans = it.get('answer','')
                                for trig in it.get('triggers',[]):
                                    trig = norm_text(trig, False)
                                    if trig and ans:
                                        items.append({'q': trig, 'a': ans})
                elif isinstance(obj, list):
                    items = obj
                self.items = items
            except json.JSONDecodeError:
                self.items = [json.loads(line) for line in txt.splitlines() if line.strip()]
                print("[llm_data] No se pudo cargar", flush=True)
        except Exception as e:
            self.items = []
            print("[llm_data] No se pudo abrir", flush=True)
    
    def lookup(self, query: str) -> Dict[str, Any]:
        """ Simple exact or fuzzy match in the GENERAL_RAG. Returns dict with 'answer' and 'score' (0.0–1.0) """
        if not self.items:
            return {"error":"general_rag_vacia","answer":"","score":FUZZY_LOGIC_ACCURACY_GENERAL_RAG}
        query = norm_text(query, False)
        best, best_s = None, 0.0

        for item in self.items:
            q = item.get('q','')
            fuzzy = (rf_fuzz.ratio(query, q)/100.0) if HAS_RF else SequenceMatcher(None, query, q).ratio()
            s = fuzzy
            if s > best_s:
                best, best_s = item, s
        print(f"[llm_data] GENERAL_RAG lookup '{query}' -> '{best.get('a','') if best else ''}' ({best_s})", flush=True)
        if best and best_s >= FUZZY_LOGIC_ACCURACY_GENERAL_RAG:
            return {"answer": best.get('a',''), "score": round(best_s,3)}
        return {"answer":"","score": round(best_s,3)}