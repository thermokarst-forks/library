FROM continuumio/miniconda3

# TODO: python 3.8

RUN conda update conda -y
RUN conda install conda-build pip -y
RUN mkdir /code
RUN mkdir /data

WORKDIR /code
COPY . /code/
RUN pip install -r requirements/local.txt
RUN apt-get update -y
RUN apt-get install procps -y
