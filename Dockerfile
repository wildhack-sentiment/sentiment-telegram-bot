FROM python:3.8-slim

ENV DATABASE_URL sqlite:////var/lib/django-db/pmdaily.sqlite
ENV CELERY_BACKEND redis://redis:6379/8

COPY src/requirements.txt ./

RUN apt-get update \
    && apt-get --no-install-recommends --assume-yes install \
      libcairo2 \
      libpango-1.0-0 \
      libpangocairo-1.0-0 \
      libgdk-pixbuf2.0-0 \
      libffi-dev \
      shared-mime-info \
    && apt-get --no-install-recommends -y install \
      build-essential \
      libpq-dev \
      python-dev \
    && apt-mark manual \
      libpq5 \
      python \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install uwsgi \
    && apt-get remove -y \
      libpq-dev \
      python-dev \
      build-essential \
    && apt-get -y autoclean && apt-get -y autoremove && apt-get -y clean

RUN pip install uwsgi
RUN pip install --no-cache-dir -r requirements.txt

ADD src /srv

ENV NO_CACHE=On
RUN python3 srv/manage.py collectstatic --noinput
ENV NO_CACHE=Off

WORKDIR /srv
