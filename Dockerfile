FROM python:3.10-slim

RUN apt update && apt install libmaxminddb0 libmaxminddb-dev mmdb-bin

RUN pip install poetry --no-cache-dir
RUN poetry config virtualenvs.create false

WORKDIR /app

COPY poetry.lock .
COPY pyproject.toml .
RUN poetry install

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]