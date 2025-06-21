# syntax=docker/dockerfile:1
FROM python:3.11-slim-bullseye

# ----- metadata -----
LABEL maintainer="Bharath Bhaskar"
WORKDIR /app

# ----- Python deps -----
COPY requirements.txt .
COPY pytest.ini .            

RUN pip install --no-cache-dir -r requirements.txt

# ----- project source -----
COPY ./app    ./app
COPY ./alembic.ini ./
COPY ./alembic ./alembic
COPY ./tests  ./tests
COPY ./docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh           

# ----- Alembic entrypoint -----
COPY ./docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT [ "docker-entrypoint.sh" ]

# Default command starts the API (can be overridden in docker-compose)
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
