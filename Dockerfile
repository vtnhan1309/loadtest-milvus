FROM python:3.8-slim as builder

RUN apt-get update -y && apt-get install -y git python3-pip ffmpeg libsm6 libxext6

WORKDIR /loadtest

COPY . .
RUN pip3 install -r requirements.txt
