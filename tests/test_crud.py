# tests/test_crud.py
import pytest
from unittest.mock import MagicMock

from app import crud, models, schemas

class DummySession:
    """A minimal fake Session for testing."""
    def __init__(self):
        self.added = []
        self.committed = False

    def add(self, obj):
        self.added.append(obj)

    def commit(self):
        self.committed = True

    def refresh(self, obj):
        pass

def test_create_candidate_unit():
    session = DummySession()
    cand_schema = schemas.CandidateCreate(
        first_name="Unit",
        last_name="Tester",
        email="unit@test.com",
        phone="1234"
    )
    cand = crud.create_candidate(session, cand_schema)

    # Check type and field values
    assert isinstance(cand, models.Candidate)
    assert cand.email == "unit@test.com"
    assert session.committed
    assert cand in session.added

def test_create_resume_unit():
    session = DummySession()
    resume_schema = schemas.ResumeCreate(
        candidate_id=1,
        title="Sample Resume",
        file_url="https://unit.test/resume.pdf"
    )
    resume = crud.create_resume(session, resume_schema)
    assert isinstance(resume, models.Resume)
    assert resume.title == "Sample Resume"
    assert session.committed
