FROM --platform=linux/amd64 python:3.11.9-alpine3.20

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir -U pip setuptools wheel
RUN pip install --no-cache-dir uvicorn[standard]

COPY requirements.txt ./

RUN python -m venv /venv && \
    pip install --no-cache-dir -r requirements.txt
ENV PATH="/venv/bin:$PATH"

COPY api api
COPY pyproject.toml .

RUN addgroup -g 1001 -S appuser && \
    adduser -u 1001 -G appuser -s /sbin/nologin -D appuser

RUN chown -R appuser:appuser /app

USER appuser

RUN find . -type d -exec chmod 755 {} \; && \
    find . -type f -exec chmod 644 {} \;

EXPOSE 8000

CMD ["uvicorn", "--host", "0.0.0.0", "--workers", "4", "--use-colors", "api.app:app"]
