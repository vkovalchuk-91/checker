FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONDUNBUFFERED 1

WORKDIR /code

COPY requirements requirements

RUN pip install --upgrade pip && \
    pip install -r requirements/development.txt --no-cache-dir

COPY . .

EXPOSE 8000