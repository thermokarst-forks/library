# This Dockerfile is for deployment purposes
FROM continuumio/miniconda3

RUN conda update conda -y
RUN conda install conda-build pip -y
RUN mkdir /code
RUN mkdir /data

WORKDIR /code
COPY . /code/
RUN pip install -r requirements/production.txt
RUN apt-get update -y
RUN apt-get install procps -y

EXPOSE 8000
