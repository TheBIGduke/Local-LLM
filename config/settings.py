import os
#THIS IS THE CONFIG FILE
#Here you can control everything of the LLM Package

"""Global"""
LANGUAGE = "es" #The code is actually not prepared to work with other languages, but for future improvements
MODELS_PATH = "config/models.yml"

"""Audio Listener is the node to hear something from the MIC"""
AUDIO_LISTENER_DEVICE_ID: int | None = None #The system is prepared to detect the best device, but if you want to force a device, put the id here
AUDIO_LISTENER_CHANNELS = 1 # "mono" or "stereo"
AUDIO_LISTENER_SAMPLE_RATE = 16000
AUDIO_LISTENER_FRAMES_PER_BUFFER = 1000

"""LLM"""
USE_LLM = True #If you disable this flag, and the question is not in the Categories we don't call the general knowledge.
CONTEXT_LLM = 1024 #The size of the context that your model is going to receive
THREADS_LLM = os.cpu_count() or 8 #Threads that has available your model 
N_BATCH_LLM = 512 #The size of the info that gpu or cpu is going to process
GPU_LAYERS_LLM = 0 #How many layers your model is going to use in GPU, for CPU use "0"
CHAT_FORMAT_LLM = "chatml-function-calling" #NOT recommended to change unless you change the model

"""Information - data"""
FUZZY_LOGIC_ACCURACY_GENERAL_RAG = 0.60 # Configure the priority of LLM over the RAG
PATH_GENERAL_RAG = "config/data/general_rag.json"

"""Text-to-Speech"""
SAMPLE_RATE_TTS = 24000
DEVICE_SELECTOR_TTS = "cpu" # "cpu" or "cuda"
VOLUME_TTS = 2.0 #Volume  of the TTS
SPEED_TTS = 1.0 # 1.0 = Fast and 2.0 = slow
PATH_TO_SAVE_TTS = "tts/audios" #Specify the PATH where we are going to save the Info
NAME_OF_OUTS_TTS = "test" #This is the name that your file is going to revive Ex: test_0.wav -> A subfolder /test is gonna be created
SAVE_WAV_TTS = False

"""Speech-to-Text"""
SAMPLE_RATE_STT = 16000 #Whisper works at this sample_rate doesn't change unless it is necessary
#IMPORTANT the system is prepare to work without this variable, but we have it for noisy environments, as a protection method
LISTEN_SECONDS_STT = 5.0 #The time of the phrase that the tts is going to be active after de wake_word detection
MIN_SILENCE_MS_TO_DRAIN_STT = 100 # 1s of time required to drain the buffer. Its divided by 10 because we sample at 10ms
SELF_VOCABULARY_STT = "Octybot, ve a la enfermería, DatIA Demographics" 

"""Wake-Word"""
ACTIVATION_PHRASE_WAKE_WORD = "ok robot" #The Activation Word that the model is going to detect
VARIANTS_WAKE_WORD =  ["ok robot", "okay robot", "hey robot"] #variations

""""Use Avatar"""
AVATAR = False #If you want to use the avatar