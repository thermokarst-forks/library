FROM continuumio/miniconda3

ARG RUNENV=production

RUN apt-get update -y
RUN apt-get install procps -y
RUN conda update conda -y
RUN conda install conda-build pip -y

RUN mkdir /code
RUN mkdir /data

WORKDIR /code
COPY . /code/

ENV DJANGO_SETTINGS_MODULE "config.settings.${RUNENV}"
RUN pip install -r "requirements/${RUNENV}.txt"

EXPOSE 8000
