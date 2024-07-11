FROM python:3.12.4-alpine
EXPOSE 5000
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
RUN apk update && \
    apk add --no-cache iputils
ENV PYTHONPATH /app
CMD ["/bin/sh", "docker-entrypoint.sh"]