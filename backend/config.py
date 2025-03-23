import os

from dotenv import load_dotenv

load_dotenv()

OPENAPI_BASE_URL = os.getenv("OPENAPI_BASE_URL")
OPENAPI_KEY = os.getenv("OPENAPI_KEY")
OPENAPI_MODEL = os.getenv("OPENAPI_MODEL")
OPENAPI_EMBEDDING_MODEL = os.getenv("OPENAPI_EMBEDDING_MODEL")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_URI = os.getenv("NEO4J_URI")
