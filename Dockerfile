FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry install --no-interaction
RUN mkdir -p /app/media && \
  mkdir -p /app/static

COPY . /app
EXPOSE 8000
RUN poetry run python /app/manage.py migrate
ENTRYPOINT poetry run python /app/manage.py runserver 0.0.0.0:8000