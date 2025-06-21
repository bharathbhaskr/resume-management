from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Candidate(Base):
    __tablename__ = "candidates"
    candidate_id = Column(Integer, primary_key=True, index=True)
    first_name   = Column(String, nullable=False)
    last_name    = Column(String, nullable=False)
    email        = Column(String, unique=True, nullable=False, index=True)
    phone        = Column(String)
    created_at   = Column(DateTime, default=datetime.utcnow)
    updated_at   = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resumes      = relationship("Resume", back_populates="candidate", cascade="all, delete")

class Resume(Base):
    __tablename__ = "resumes"
    resume_id    = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.candidate_id", ondelete="CASCADE"), nullable=False)
    title        = Column(String, nullable=False)
    file_url     = Column(String, nullable=False)
    uploaded_at  = Column(DateTime, default=datetime.utcnow)
    candidate    = relationship("Candidate", back_populates="resumes")
