FROM python:3.11.8-slim AS build
ARG POETRY_VERSION=1.7.1
ENV POETRY_VENV=/opt/poetry-venv

RUN apt-get update && \
  apt-get install --no-install-suggests --no-install-recommends --yes && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* && \
  python3 -m venv "${POETRY_VENV}" \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install "poetry==${POETRY_VERSION}"

ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Copy over poetry configuration
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && poetry install

# Copy over additional files
COPY /app /opt/app

FROM gcr.io/distroless/python3-debian12:debug AS deploy
ENV POETRY_VENV=/opt/poetry-venv


COPY --from=build ${POETRY_VENV} ${POETRY_VENV}
COPY --from=build /opt /opt

ENV PATH="${PATH}:${POETRY_VENV}/bin"
ENV PYTHONPATH=/app:/opt/poetry-venv/lib/python3.11/site-packages

WORKDIR /opt

ENTRYPOINT ["/usr/bin/python3.11", "poetry", "run"]
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8080"]
