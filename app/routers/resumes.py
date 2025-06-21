from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, crud, db

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

    cand = crud.get_candidate(session, res_in.candidate_id)
    if not cand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    return crud.create_resume(session, res_in)


@router.get(
    "/",
    response_model=list[schemas.ResumeOut]
)
def read_resumes(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(db.get_db),
):
    return crud.list_resumes(session, skip, limit)


@router.get(
    "/{resume_id}",
    response_model=schemas.ResumeOut
)
def read_resume(
    resume_id: int,
    session: Session = Depends(db.get_db),
):
    r = crud.get_resume(session, resume_id)
    if not r:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    return r


@router.delete(
    "/{resume_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_resume(
    resume_id: int,
    session: Session = Depends(db.get_db),
):
    r = crud.get_resume(session, resume_id)
    if not r:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    crud.delete_resume(session, resume_id)
    return
