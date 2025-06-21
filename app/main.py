from fastapi import FastAPI
from app.db import engine
from app.models import Base
from app.routers import candidates, resumes
import logging

Base.metadata.create_all(bind=engine)

logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more verbosity
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("resume-management")


app = FastAPI(title="Candidate & Resume API")
app.include_router(candidates.router) 
app.include_router(resumes.router)
