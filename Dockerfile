FROM python:3.9-bullseye

ARG APP_PATH=/github.com/merklebot/call_joiner/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.11 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

ENV TZ "UTC"
RUN echo "${TZ}" > /etc/timezone \
  && dpkg-reconfigure --frontend noninteractive tzdata

RUN apt-get update -y && \
    apt-get install -y chromium chromium-driver

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR $APP_PATH

COPY pyproject.toml poetry.lock $APP_PATH

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY . $APP_PATH

CMD ["python", "-m", "call_joiner"]
