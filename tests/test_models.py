# tests/test_models.py
from app.models import Candidate, Resume, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def test_cascade_delete():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    # Create candidate and resume
    cand = Candidate(first_name="Test", last_name="C", email="c@unit.test", phone="0000")
    db.add(cand)
    db.commit()
    db.refresh(cand)
    res = Resume(candidate_id=cand.candidate_id, title="Unit", file_url="x.pdf")
    db.add(res)
    db.commit()

    # Delete candidate
    db.delete(cand)
    db.commit()

    # Resume should be gone
    assert db.query(Resume).filter_by(candidate_id=cand.candidate_id).first() is None
