#!/usr/bin/env bash
set -e

# Wait for Postgres if DATABASE_URL points there
if [[ "$DATABASE_URL" == postgresql* ]]; then
  echo "waiting for database..."
  until python - <<'PY'
import os, sys, sqlalchemy as sa, time
url = os.environ["DATABASE_URL"]
for _ in range(90):
    try:
        sa.create_engine(url, pool_pre_ping=True).connect()
        sys.exit(0)
    except Exception as e:
        time.sleep(1)
sys.exit("DB never became available") 
PY
  do
    sleep 1
  done
fi

# Run migrations (no-op for SQLite)
alembic upgrade head

exec "$@"
