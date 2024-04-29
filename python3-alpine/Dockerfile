ARG POETRY_VERSION=1.8.2
ARG PROJECT_NAME=alpine-version
ARG PY_VER_FULL=3.11.8
ARG PY_VER_MAJOR=3.11

FROM python:3.11.8-alpine3.19 as base
ARG PY_VER_MAJOR
ARG PY_ROOT_MODULE

ENV PROJECT_HOME=/opt/${PROJECT_NAME}
ENV PROJECT_PYTHONPATH=${PROJECT_HOME}/.venv/lib/python${PY_VER_MAJOR}/site-packages
ENV PROJECT_VENV_BIN=${PROJECT_HOME}/.venv/bin
# prefix the venv bin to the path
ENV PATH=${PROJECT_VENV_BIN}${PATH:+":$PATH"}

RUN mkdir --parents ${PROJECT_VENV_BIN} && pip install poetry==1.8.2
WORKDIR ${PROJECT_HOME}

# ================================================================
# Builder image
# adds python project files
# ================================================================
FROM base as builder

# separate caching layer for deps
COPY pyproject.toml poetry.lock ./

RUN poetry install --only=main --no-root

# caching layer for root
COPY ${PY_ROOT_MODULE} ${PY_ROOT_MODULE}/

# ================================================================
# Dev Image
# adds testing, linting related files
# ================================================================
FROM builder as dev

ARG PY_ROOT_MODULE
ARG PROJECT_NAME

RUN poetry install

# Only for running CI steps
# COPY tests tests/

# ================================================================
# Prod Image
# only module and venv related files
# ================================================================
FROM alpine:3.19 as prod
ARG PY_VER_MAJOR
ARG PROJECT_NAME

# force install to local since it matches layer above
ENV PATH=/usr/local/bin:$PATH

# Manually install python3 and create a symbolic link to where it should be
RUN apk update && apk add --no-cache python3  && ln -s /usr/bin/python /usr/local/bin/python

# Creates new paths for caching layer
ENV PROJECT_HOME=/opt/${PROJECT_NAME}
ENV PROJECT_PYTHONPATH=${PROJECT_HOME}/.venv/lib/python${PY_VER_MAJOR}/site-packages
ENV PROJECT_VENV_BIN=${PROJECT_HOME}/.venv/bin
ENV PATH=${PROJECT_VENV_BIN}${PATH:+":$PATH"}
RUN mkdir --parents ${PROJECT_VENV_BIN}

WORKDIR ${PROJECT_HOME}

# Pull dependencies cached from previous layer
COPY --from=builder ${PROJECT_PYTHONPATH} ${PROJECT_PYTHONPATH}
COPY --from=builder ${PROJECT_VENV_BIN} ${PROJECT_VENV_BIN}/
COPY --from=builder "${PROJECT_HOME}/${PY_ROOT_MODULE}" ${PY_ROOT_MODULE}/

# # Run container as a non-root user
RUN adduser -D appuser
RUN chown appuser:appuser ${PROJECT_HOME} && chmod 700 ${PROJECT_HOME}
USER appuser

# allow invoking without poetry, e.g. can use simply `python -m` instead of `poetry run python -m`
ENV PYTHONPATH=${PROJECT_PYTHONPATH}${PYTHONPATH:+":$PYTHONPATH"}

# # gunicorn --bind=0.0.0.0:8000 app.api.main:app