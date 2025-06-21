from sqlalchemy.orm import Session
from app import models, schemas

# Candidates
def create_candidate(db: Session, cand: schemas.CandidateCreate):
    candidate = models.Candidate(**cand.dict())
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate

def list_candidates(db: Session, skip=0, limit=100):
    return db.query(models.Candidate).offset(skip).limit(limit).all()

def get_candidate(db: Session, candidate_id: int):
    return db.query(models.Candidate).filter(models.Candidate.candidate_id == candidate_id).first()

def update_candidate(db: Session, candidate_id: int, cand: schemas.CandidateCreate):
    candidate = db.query(models.Candidate).filter(models.Candidate.candidate_id == candidate_id).first()
    if candidate:
        for key, value in cand.dict().items():
            setattr(candidate, key, value)
        db.commit()
        db.refresh(candidate)
    return candidate

def delete_candidate(db: Session, candidate_id: int):
    candidate = db.query(models.Candidate).filter(models.Candidate.candidate_id == candidate_id).first()
    if candidate:
        db.delete(candidate)
        db.commit()

# Resumes
def create_resume(db: Session, res: schemas.ResumeCreate):
    resume = models.Resume(
        candidate_id=res.candidate_id,
        title=res.title,
        file_url=str(res.file_url)  # <-- convert HttpUrl explicitly to string
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    return resume

def list_resumes(db: Session, skip=0, limit=100):
    return db.query(models.Resume).offset(skip).limit(limit).all()

def get_resume(db: Session, resume_id: int):
    return db.query(models.Resume).filter(models.Resume.resume_id == resume_id).first()

def update_resume(db, resume_id, resume_in):
    resume = db.query(models.Resume).filter_by(resume_id=resume_id).first()
    if not resume:
        return None
    resume.title = resume_in.title
    resume.file_url = str(resume_in.file_url)
    db.commit()
    db.refresh(resume)
    return resume

def delete_resume(db: Session, resume_id: int):
    resume = db.query(models.Resume).filter(models.Resume.resume_id == resume_id).first()
    if resume:
        db.delete(resume)
        db.commit()
