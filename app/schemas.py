from pydantic import BaseModel, EmailStr, HttpUrl
from typing import List, Optional
from datetime import datetime

class ResumeOut(BaseModel):
    resume_id: int
    title: str
    file_url: str
    uploaded_at: datetime
    class Config:
        orm_mode = True

class ResumeCreate(BaseModel):
    candidate_id: int
    title: str
    file_url: HttpUrl       

    class Config:
        from_attributes = True   

class CandidateCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None

class CandidateOut(CandidateCreate):
    candidate_id: int
    created_at: datetime
    updated_at: datetime
    resumes: List[ResumeOut] = []
    class Config:
        orm_mode = True
