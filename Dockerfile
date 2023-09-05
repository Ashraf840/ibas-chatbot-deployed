FROM ubuntu:20.04

RUN mkdir /chatbot
WORKDIR /chatbot

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./requirements.txt
RUN apt update && apt install python3 python3-pip python3-dev -y
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

COPY models ./models
COPY actions ./actions
COPY config.yml ./config.yml
COPY endpoints.yml ./endpoints.yml
COPY run.sh ./run.sh

CMD ["sh", "./run.sh"]
