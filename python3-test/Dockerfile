ARG PYTHON_DISTROLESS_IMAGE

FROM python:3.11.8-slim AS builder

WORKDIR /tmp
COPY poetry.lock pyproject.toml ./

ARG VIRTUAL_ENV=/home/venv

RUN pip --quiet --no-cache-dir install --upgrade pip && \
    pip --quiet --no-cache-dir install poetry && \
    poetry config virtualenvs.create false && \
    python -m venv ${VIRTUAL_ENV} && \
    . ${VIRTUAL_ENV}/bin/activate && \
    poetry install --no-root --only main

# ------------------------------------------------------------------

FROM gcr.io/distroless/python3-debian12:debug

ARG VIRTUAL_ENV=/home/venv

WORKDIR /app
COPY --chown=1000:1000 *.py /app/
COPY --chown=1000:1000 --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

ENTRYPOINT ["/home/venv/bin/python", "run.py", "-b", "0.0.0.0:5000", "app:app"]