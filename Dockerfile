FROM python:3.12.4-alpine
EXPOSE 5000
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
RUN apk update && \
    apk add --no-cache iputils
ENV DJANGO_SETTINGS_MODULE="itsanapi.settings.production"
RUN python manage.py collectstatic
CMD ["/bin/sh", "docker-entrypoint.sh"]