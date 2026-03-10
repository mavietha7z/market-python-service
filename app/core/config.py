import os
from dotenv import load_dotenv

load_dotenv()

# ========================
# API KEYS
# ========================

API_KEYS = os.getenv("API_KEYS", "").split(",")

# ========================
# CACHE
# ========================

CACHE_TTL = int(os.getenv("CACHE_TTL", 300))

# ========================
# DATA SOURCES
# ========================

VALID_SOURCES = {"KBS", "VCI"}