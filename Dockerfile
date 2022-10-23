# FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-runtime

FROM python:3.9

RUN apt-get update && \
    apt-get install -y && \
    apt-get install -y apt-utils wget && \
    apt-get -qq -y install curl && \
    apt-get install -y tar


RUN pip install --upgrade pip
RUN pip install flask \
    waitress 

WORKDIR /app
COPY . .

RUN ls -l

EXPOSE 80

CMD ["python", "main.py"]