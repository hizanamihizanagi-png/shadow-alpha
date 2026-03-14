import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import app as shadow_app
from fastapi import FastAPI

# Wrapper for Vercel to strip the /api rewrite prefix
# so that the inner routers correctly resolve /auth, /exchange, etc.
app = FastAPI()
app.mount("/api", shadow_app)
