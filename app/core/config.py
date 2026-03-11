import os
from dotenv import load_dotenv

load_dotenv()

# ========================
# API KEYS
# ========================
API_KEY = os.getenv("API_KEY", "")

# ========================
# CACHE
# ========================
CACHE_TTL = int(os.getenv("CACHE_TTL", 300))

