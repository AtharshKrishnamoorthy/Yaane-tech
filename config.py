import os

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    

    RATE_LIMIT_TPM = 15000 
    RETRY_DELAY = 1
    MAX_RETRIES = 3