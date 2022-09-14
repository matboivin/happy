FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /usr/app

COPY . .

RUN poetry install

ENTRYPOINT ["poetry", "run", "uvicorn", "--host", "127.0.0.1", "happy.main:app"]
