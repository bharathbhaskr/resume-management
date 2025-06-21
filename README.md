# Candidate & Resume Management API

A full-stack, Dockerized RESTful API built with **FastAPI** and **PostgreSQL** for managing candidates and their resumes.

> **Features:**
>
> * Candidate CRUD (Create, Read, Update, Delete)
> * Resume CRUD (linked to candidates, cascade delete)
> * Unique email enforcement
> * Swagger UI auto-docs
> * Alembic migrations
> * Docker Compose for local development
> * Production-ready structure and best practices

---

## 🚀 Quick Start

### 1. **Clone the Repo**

```bash
git clone https://github.com/bharathbhaskr/resume-management.git
cd resume-management
```

### 2. **Run with Docker Compose**

> **Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.**

```bash
docker compose up --build
```

* API will be live at [http://localhost:8000](http://localhost:8000)
* Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)
* Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 3. **Stop and Clean Up**

```bash
docker compose down -v
```

---

## 🏗️ Project Structure

```
resume-management/
├── app/
│   ├── main.py             # FastAPI app setup & routers
│   ├── models.py           # SQLAlchemy models
│   ├── schemas.py          # Pydantic schemas
│   ├── crud.py             # DB access logic (CRUD)
│   ├── db.py               # DB session/engine
│   └── routers/
│       ├── candidates.py   # Candidate API endpoints
│       └── resumes.py      # Resume API endpoints
├── alembic/                # DB migrations
│   └── versions/
├── alembic.ini
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── docker-entrypoint.sh
├── tests/
│   └── test_api.py         # Pytest API tests
└── README.md
```

---

## ⚙️ Environment Variables

Set in `docker-compose.yml`:

```yaml
POSTGRES_DB=resume_db
POSTGRES_USER=resume_admin
POSTGRES_PASSWORD=bharath
DATABASE_URL=postgresql+psycopg2://resume_admin:bharath@db:5432/resume_db
```

---

## 🗂️ API Endpoints

### Candidates

* `POST /candidates/` — Create new candidate
* `GET /candidates/` — List all candidates
* `GET /candidates/{candidate_id}` — Get candidate by ID
* `PUT /candidates/{candidate_id}` — Update candidate
* `DELETE /candidates/{candidate_id}` — Delete candidate & all their resumes (cascade)

### Resumes

* `POST /resumes/` — Add resume for candidate
* `GET /resumes/` — List all resumes
* `GET /resumes/{resume_id}` — Get resume by ID

See **Swagger UI** at `/docs` for detailed request/response examples.

---

## 🧪 Testing

* Tests use **pytest** and **httpx**.

* To run inside Docker:

  ```bash
  docker compose run --rm test
  ```

* Or, run locally (make sure `pytest` and `httpx` are installed):

  ```bash
  pytest
  ```

---

## 🔐 Data Integrity & Validation

* **Unique emails:** Duplicate emails return HTTP 400.
* **Cascade delete:** Deleting a candidate deletes all their resumes.
* **Resume:** Cannot be created for non-existent candidate (HTTP 404).
* **All validation** via Pydantic & FastAPI.

---

## 🛠️ Database Migrations

* Handled by **Alembic**.
* On startup, Docker entrypoint waits for DB & runs `alembic upgrade head`.

---

## 🐳 Docker Details

* `web` service runs FastAPI + Uvicorn.
* `db` service runs Postgres 16.
* Volumes support hot-reloading code in development.
* All secrets/configs set via `docker-compose.yml` (override with `.env` if needed).

---

## 📑 Example API Calls (for Postman/cURL)

### Create Candidate

```http
POST http://localhost:8000/candidates/
Content-Type: application/json

{
  "first_name": "Testt",
  "last_name": "User",
  "email": "test@example.com",
  "phone": "555-1111"
}
```

### Create Resume

```http
POST http://localhost:8000/resumes/
Content-Type: application/json

{
  "candidate_id": 1,
  "title": "Backend Resume",
  "file_url": "https://example.com/resume.pdf"
}
```

## 🙋‍♂️ Author

* [Bharath Bhaskar](https://github.com/bharathbhaskr)

---

## 📝 License

MIT License (or your choice)

---
