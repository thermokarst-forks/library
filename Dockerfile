# This Dockerfile is for deployment purposes
FROM continuumio/miniconda3

RUN apt-get update -y
RUN apt-get install procps -y
RUN conda update conda -y
RUN conda install conda-build pip -y

RUN mkdir /code
RUN mkdir /data

WORKDIR /code
COPY . /code/

RUN if [ "$DJANGO_SETTINGS_MODULE" = "config.settings.production" ] ; \
    then pip install -r requirements/production.txt ; \
    else pip install -r requirements/local.txt ; fi

EXPOSE 8000
