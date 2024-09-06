ARG PROJECT_NAME=python3-slim-uv
ARG PY_ROOT_MODULE=app
ARG PY_VER_FULL=3.11.9
ARG PY_VER_MAJOR=3.11
ARG UV_VERSION=0.4.6

# ===================
# Setup Layer
# ===================
FROM python:3.11.9 as base
ARG PROJECT_NAME
ARG PY_VER_MAJOR
ARG UV_VERSION

RUN apt-get install -y --no-install-recommends wget

RUN pip install uv==${UV_VERSION}
WORKDIR ${HOME}

# ===================
# Builder image
# ===================
FROM base as builder
ARG PY_ROOT_MODULE

COPY pyproject.toml uv.lock ./

RUN uv venv --python $(python --version | cut -d ' ' -f2) && \
uv sync --frozen

COPY ${PY_ROOT_MODULE} ${PY_ROOT_MODULE}/

# ===================
# Prod Image
# ===================

FROM python:3.11.9-slim as prod
ARG PROJECT_NAME
ARG PY_ROOT_MODULE
ARG PY_VER_MAJOR

ENV PROJ_PYTHONPATH=/.venv/lib/python${PY_VER_MAJOR}/site-packages

# Pull dependencies cached from previous layer

# Needed for cron job build
RUN apt-get update && apt-get install -y --no-install-recommends wget

COPY --from=builder ${PROJ_PYTHONPATH} ${PROJ_PYTHONPATH}
COPY --from=builder "${PY_ROOT_MODULE}" ${PY_ROOT_MODULE}/

ENV PYTHONPATH=${PROJ_PYTHONPATH}${PYTHONPATH:+":$PYTHONPATH"}
