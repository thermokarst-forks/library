FROM continuumio/miniconda3

ARG RUNENV=production

RUN apt-get update -y
RUN apt-get install procps postgresql-contrib -y
RUN conda update conda -y
RUN conda install conda-build pip python=3.8 -y

RUN mkdir /code
RUN mkdir /data

RUN useradd -r -s /bin/bash -g ubuntu -G ubuntu -u 1000 ubuntu
USER ubuntu:ubuntu
RUN chown ubuntu:ubuntu /data

WORKDIR /code
COPY . /code/

ENV DJANGO_SETTINGS_MODULE "config.settings.${RUNENV}"
RUN pip install -r "requirements/${RUNENV}.txt"

EXPOSE 8000
