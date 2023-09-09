# Dockerfile

FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Create an app user
RUN useradd --user-group --create-home --no-log-init --shell /bin/bash app

ENV APP_HOME=/app/src

# Create the staticfiles directory. This avoids permission errors.
RUN mkdir -p $APP_HOME/static
RUN mkdir -p $APP_HOME/media

WORKDIR $APP_HOME






COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt


COPY src $APP_HOME

RUN chmod +x /app/src/scripts/entrypoint.sh
RUN sed -i 's/\r$//g' /app/src/scripts/entrypoint.sh





RUN chown -R app:app $APP_HOME

USER app:app
EXPOSE 8000


# run entrypoint.sh
ENTRYPOINT ["/bin/bash","/app/src/scripts/entrypoint.sh"]
