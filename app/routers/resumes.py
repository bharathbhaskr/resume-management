from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, crud, db
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/resumes", tags=["resumes"])

@router.post(
    "/",
    response_model=schemas.ResumeOut,
    status_code=status.HTTP_201_CREATED
)
def upload_resume(
    res_in: schemas.ResumeCreate,
    session: Session = Depends(db.get_db),
):
    logger.info(f"Attempting to upload resume for candidate_id: {res_in.candidate_id}")
    cand = crud.get_candidate(session, res_in.candidate_id)
    if not cand:
        logger.error(f"Resume upload failed: candidate not found (candidate_id={res_in.candidate_id})")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    resume = crud.create_resume(session, res_in)
    logger.info(f"Resume uploaded successfully: {resume.resume_id} for candidate_id {res_in.candidate_id}")
    return resume

@router.get(
    "/",
    response_model=list[schemas.ResumeOut]
)
def read_resumes(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(db.get_db),
):
    logger.info(f"Listing resumes (skip={skip}, limit={limit})")
    resumes = crud.list_resumes(session, skip, limit)
    logger.info(f"Found {len(resumes)} resume(s)")
    return resumes

@router.get(
    "/{resume_id}",
    response_model=schemas.ResumeOut
)
def read_resume(
    resume_id: int,
    session: Session = Depends(db.get_db),
):
    logger.info(f"Fetching resume with ID: {resume_id}")
    r = crud.get_resume(session, resume_id)
    if not r:
        logger.error(f"Resume not found: {resume_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    logger.info(f"Resume retrieved: {r.resume_id} (candidate_id={r.candidate_id})")
    return r

@router.put(
    "/{resume_id}",
    response_model=schemas.ResumeOut
)
def update_resume(
    resume_id: int,
    resume_in: schemas.ResumeCreate,
    session: Session = Depends(db.get_db),
):
    logger.info(f"Attempting to update resume {resume_id} with data: {resume_in}")
    r = crud.get_resume(session, resume_id)
    if not r:
        logger.warning(f"Resume not found for update: {resume_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    updated_resume = crud.update_resume(session, resume_id, resume_in)
    logger.info(f"Resume {resume_id} updated successfully.")
    return updated_resume

@router.delete(
    "/{resume_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_resume(
    resume_id: int,
    session: Session = Depends(db.get_db),
):
    logger.info(f"Deleting resume with ID: {resume_id}")
    r = crud.get_resume(session, resume_id)
    if not r:
        logger.error(f"Resume not found for deletion: {resume_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    crud.delete_resume(session, resume_id)
    logger.info(f"Resume deleted successfully: {resume_id}")
    return
