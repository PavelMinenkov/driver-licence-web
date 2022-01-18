FROM python:3.8

ADD app /app
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt && \
    chmod +x /app/wait-for-it.sh

WORKDIR /app

ENV DJANGO_SETTINGS_MODULE='settings.production'

HEALTHCHECK --interval=30s --timeout=15s --start-period=30s --retries=2 \
  CMD curl -f http://localhost:$WSGI_PORT/maintenance/check_health/ || exit 1

# FIRE!!!
CMD echo "Wait database is ready" && /app/wait-for-it.sh ${DATABASE_HOST}:${DATABASE_PORT-5432} --timeout=60 && \
  cd /app && \
  echo "Database migration" && python manage.py migrate && \
  echo "Run server" && uvicorn settings.asgi:application --reload --port=80 --host=0.0.0.0