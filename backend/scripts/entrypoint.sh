#!/bin/sh

set -e
set -x

# Run migrations alembic
.venv/bin/alembic upgrade head

# Run the application
exec su-exec sfuser .venv/bin/uvicorn \
    --host 0.0.0.0 \
    --workers 4 \
    --forwarded-allow-ips='*' \
    app.main:app
