FROM python:3.10

ARG PIP_NO_CACHE_DIR=off
ARG PIP_DISABLE_PIP_VERSION_CHECK=on
ARG POETRY_VERSION

RUN pip install "poetry==$POETRY_VERSION"

ARG REPO_DIR=/moviesvault
WORKDIR ${REPO_DIR}
COPY pyproject.toml ${REPO_DIR}

# Project initialization:
ARG PROJECT_ENV
RUN poetry config virtualenvs.create false \
  && poetry install $(if [ "$PROJECT_ENV" == production ]; then echo "--no-dev"; fi) --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY . /code