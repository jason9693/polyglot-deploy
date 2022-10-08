FROM python:3.9-alpine

RUN apt-get update && \
    apt-get install -y && \
    apt-get install -y apt-utils wget && \
    apt-get -qq -y install curl && \
    apt-get install -y tar


RUN pip install --upgrade pip
RUN pip install transformers==3.5.0 \
    flask \
    waitress 

WORKDIR /app
COPY . .

RUN ls -l

EXPOSE 80

CMD ["python", "main.py"]