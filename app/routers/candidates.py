from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, crud, db

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
    # 400 if email already exists
    if session.query(models.Candidate).filter_by(email=cand.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    return crud.create_candidate(session, cand)


@router.get(
    "/", 
    response_model=list[schemas.CandidateOut]
)
def read_candidates(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(db.get_db),
):
    return crud.list_candidates(session, skip, limit)


@router.get(
    "/{candidate_id}", 
    response_model=schemas.CandidateOut
)
def read_candidate(
    candidate_id: int,
    session: Session = Depends(db.get_db),
):
    c = crud.get_candidate(session, candidate_id)
    if not c:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
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
    c = crud.get_candidate(session, candidate_id)
    if not c:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    # if updating email, ensure uniqueness
    if cand_in.email != c.email and session.query(models.Candidate).filter_by(email=cand_in.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    return crud.update_candidate(session, candidate_id, cand_in)


@router.delete(
    "/{candidate_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_candidate(
    candidate_id: int,
    session: Session = Depends(db.get_db),
):
    c = crud.get_candidate(session, candidate_id)
    if not c:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    crud.delete_candidate(session, candidate_id)
    return
