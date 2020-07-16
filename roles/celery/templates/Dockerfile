FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
RUN mkdir /data
WORKDIR /code
COPY . /code/
RUN pip install -r requirements/local.txt
