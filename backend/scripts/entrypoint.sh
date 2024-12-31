#!/bin/bash

set -e
set -x

# Run migrations alembic
alembic upgrade head

python app/helpers/seed.py

# Run the application
exec runuser -u sfuser -- uvicorn \
    --host 0.0.0.0 \
    --workers 4 \
    --forwarded-allow-ips='*' \
    app.main:app
