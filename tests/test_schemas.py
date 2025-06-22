# tests/test_schemas.py
import pytest
from pydantic import ValidationError
from app.schemas import CandidateCreate

def test_valid_candidate_schema():
    cand = CandidateCreate(
        first_name="Alice",
        last_name="Smith",
        email="alice@unit.com",
        phone="1234"
    )
    assert cand.first_name == "Alice"
    assert cand.email.endswith("@unit.com")

def test_invalid_email():
    with pytest.raises(ValidationError):
        CandidateCreate(
            first_name="X",
            last_name="Y",
            email="invalid-email",
            phone="0000"
        )

def test_first_name_type():
    with pytest.raises(ValidationError):
        CandidateCreate(
            first_name=1234,
            last_name="Smith",
            email="smith@unit.test",
            phone="1234"
        )
