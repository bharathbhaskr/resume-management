from fastapi import FastAPI
from app.db import engine
from app.models import Base
from app.routers import candidates, resumes

# Create tables if they don't exist (only for dev convenience)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Candidate & Resume API")
app.include_router(candidates.router)
app.include_router(resumes.router)
