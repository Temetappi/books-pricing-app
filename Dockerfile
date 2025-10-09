FROM python:3.12

ENV PYTHONUNBUFFERED=1

RUN pip install poetry==2.2.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app/

ENV PYTHONPATH=/app

ENV PATH="/app/.venv/bin:$PATH"

COPY ./scripts /app/scripts

COPY ./pyproject.toml ./alembic.ini /app/

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR


COPY ./app /app/app
COPY ./tests /app/tests

RUN poetry install --without dev

CMD ["fastapi", "run", "--workers", "1", "app/main.py", "--port", "8080"]
