FROM python:3.11.4-slim-buster

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

ENV DJANGO_SETTINGS_MODULE config.settings

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /usr/local/bin/wait-for-it
RUN chmod +x /usr/local/bin/wait-for-it

COPY . .

CMD gunicorn main:app --workers 2 --bind=0.0.0.0:80