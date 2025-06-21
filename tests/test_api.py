# tests/test_api.py
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app           # FastAPI application
from app.db import get_db          # original dependency
from app.models import Base        # ORM metadata

# --------------------------------------------------------------------------- #
TEST_DB_URL = "sqlite:///./tests.db"
engine = create_engine(
    TEST_DB_URL, connect_args={"check_same_thread": False}, pool_pre_ping=True
)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Build all tables once per test session
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Yield a database session bound to the test engine."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the dependency *before* creating the TestClient
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# --------------------------------------------------------------------------- #
#API endpoint checks
# --------------------------------------------------------------------------- #
def _create_candidate(email: str = "alice@example.com"):
    payload = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": email,
        "phone": "555-555-5555",
    }
    return client.post("/candidates/", json=payload)


def _create_resume(candidate_id: int, title: str = "Alice Resume"):
    payload = {
        "candidate_id": candidate_id,
        "title": title,
        "file_url": "https://example.com/alice.pdf",
    }
    return client.post("/resumes/", json=payload)


# --------------------------------------------------------------------------- #
# Candidate CRUD
# --------------------------------------------------------------------------- #
def test_create_candidate_and_duplicate_email():
    """Happy-path creation + duplicate e-mail rejection (400)."""
    # create
    r1 = _create_candidate()
    assert r1.status_code == 201
    cid = r1.json()["candidate_id"]

    # duplicate e-mail
    r2 = _create_candidate()
    assert r2.status_code == 400
    assert r2.json()["detail"] == "Email already exists"

    # read list contains at least our candidate
    r_list = client.get("/candidates/")
    assert r_list.status_code == 200
    assert any(c["candidate_id"] == cid for c in r_list.json())


def test_update_and_delete_candidate():
    """Phone update persists, then hard delete removes record."""
    cid = _create_candidate("bob@example.com").json()["candidate_id"]

    # update phone
    upd = {
        "first_name": "Bob",
        "last_name": "Jones",
        "email": "bob@example.com",
        "phone": "999-999-0000",
    }
    r_upd = client.put(f"/candidates/{cid}", json=upd)
    assert r_upd.status_code == 200
    assert r_upd.json()["phone"] == "999-999-0000"

    # delete
    r_del = client.delete(f"/candidates/{cid}")
    assert r_del.status_code == 204

    # gone
    r_get = client.get(f"/candidates/{cid}")
    assert r_get.status_code == 404


# --------------------------------------------------------------------------- #
# Resume flow + cascade behaviour
# --------------------------------------------------------------------------- #
def test_resume_lifecycle_and_cascade_delete():
    """Resume survives create/read, but is removed when candidate is deleted."""
    cid = _create_candidate("charlie@example.com").json()["candidate_id"]
    rid = _create_resume(cid).json()["resume_id"]

    # sanity check resume exists
    assert client.get(f"/resumes/{rid}").status_code == 200

    # delete candidate → cascade deletes resume (ON DELETE CASCADE) :contentReference[oaicite:1]{index=1}
    client.delete(f"/candidates/{cid}")

    # resume now 404
    assert client.get(f"/resumes/{rid}").status_code == 404


# --------------------------------------------------------------------------- #
# Clean-up once all tests have run
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="session", autouse=True)
def _drop_test_db():
    """Drop tables & remove file after the entire pytest session ends."""
    yield
    Base.metadata.drop_all(bind=engine)
    try:
        os.remove("tests.db")
    except FileNotFoundError:
        pass
