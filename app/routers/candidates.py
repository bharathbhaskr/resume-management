from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, crud, db
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/candidates", tags=["candidates"])

@router.post(
    "/", 
    response_model=schemas.CandidateOut, 
    status_code=status.HTTP_201_CREATED 
)
def create_candidate(
    cand: schemas.CandidateCreate,
    session: Session = Depends(db.get_db),
):
    logger.info(f"Attempting to create candidate: {cand.email}")
    # 400 if email already exists
    if session.query(models.Candidate).filter_by(email=cand.email).first():
        logger.warning(f"Duplicate email attempted: {cand.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    candidate = crud.create_candidate(session, cand)
    logger.info(f"Candidate created successfully: {candidate.candidate_id} ({candidate.email})")
    return candidate

@router.get(
    "/", 
    response_model=list[schemas.CandidateOut]
)
def read_candidates(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(db.get_db),
):
    logger.info(f"Listing candidates (skip={skip}, limit={limit})")
    candidates = crud.list_candidates(session, skip, limit)
    logger.info(f"Found {len(candidates)} candidate(s)")
    return candidates

@router.get(
    "/{candidate_id}", 
    response_model=schemas.CandidateOut
)
def read_candidate(
    candidate_id: int,
    session: Session = Depends(db.get_db),
):
    logger.info(f"Fetching candidate with ID: {candidate_id}")
    c = crud.get_candidate(session, candidate_id)
    if not c:
        logger.error(f"Candidate not found: {candidate_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    logger.info(f"Candidate retrieved: {c.candidate_id} ({c.email})")
    return c

@router.put(
    "/{candidate_id}",
    response_model=schemas.CandidateOut
)
def update_candidate(
    candidate_id: int,
    cand_in: schemas.CandidateCreate,
    session: Session = Depends(db.get_db),
):
    logger.info(f"Updating candidate ID: {candidate_id}")
    c = crud.get_candidate(session, candidate_id)
    if not c:
        logger.error(f"Candidate not found for update: {candidate_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    # if updating email, ensure uniqueness
    if cand_in.email != c.email and session.query(models.Candidate).filter_by(email=cand_in.email).first():
        logger.warning(f"Email update conflict for candidate {candidate_id}: {cand_in.email} already exists.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    updated = crud.update_candidate(session, candidate_id, cand_in)
    logger.info(f"Candidate updated successfully: {candidate_id}")
    return updated

@router.delete(
    "/{candidate_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_candidate(
    candidate_id: int,
    session: Session = Depends(db.get_db),
):
    logger.info(f"Deleting candidate ID: {candidate_id}")
    c = crud.get_candidate(session, candidate_id)
    if not c:
        logger.error(f"Candidate not found for deletion: {candidate_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    crud.delete_candidate(session, candidate_id)
    logger.info(f"Candidate deleted successfully: {candidate_id}")
    return
