FROM debian:12-slim AS build
ARG POETRY_VERSION=1.7.1
ENV POETRY_VENV=/opt/poetry-venv

RUN apt-get update && \
  apt-get install --no-install-suggests --no-install-recommends --yes python3-venv gcc libpython3-dev && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* && \
  python3 -m venv "${POETRY_VENV}" \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install "poetry==${POETRY_VERSION}"

ENV PATH="${PATH}:${POETRY_VENV}/bin"
WORKDIR /app

# Copy over poetry configuration
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && poetry install

# Copy over additional files
COPY app/main.py ./

FROM gcr.io/distroless/python3-debian12:debug AS deploy

ENV POETRY_VENV=/opt/poetry-venv
COPY --from=build ${POETRY_VENV} ${POETRY_VENV}

COPY --from=build /app /app

ENV PATH="${PATH}:${POETRY_VENV}/bin"
ENV PYTHONPATH="/opt/poetry-venv/lib/python3.11/site-packages"

WORKDIR /app
CMD ["main.py"]