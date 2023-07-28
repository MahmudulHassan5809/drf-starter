FROM python:3.8


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app
RUN mkdir src


ADD requirements.txt /app


RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY src/ /app/src/


EXPOSE 8000