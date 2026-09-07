from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Check your .env file."
    )

if not ANTHROPIC_API_KEY:
    raise ValueError(
        "ANTHROPIC_API_KEY not found. Check your .env file."
    )


MODEL_NAME = "gemini-3.6-flash"

MAX_OUTPUT_TOKENS = 512

DEFAULT_BENCHMARK_LIMIT = 50

# Semantic Guard & Adaptive Compression Config
SIMILARITY_THRESHOLD = 0.80
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
DEFAULT_INITIAL_BUDGET = 0.50
FALLBACK_STRATEGY = "DISCARD"