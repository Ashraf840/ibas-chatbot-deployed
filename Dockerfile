FROM ubuntu:20.04

RUN mkdir /chatbot
WORKDIR /chatbot

# Keeps Python from generating .pyc files in the container
# ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
# ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./requirements.txt
RUN apt update && apt install python3 python3-pip python3-dev -y
RUN pip install --upgrade pip
# RUN pip install -r ./requirements.txt
# RUN pip install rasa
RUN apt install python3.8-venv
RUN python3 -m venv ./venv
# COPY venv ./venv
RUN . ./venv/bin/activate
RUN pip3 install -U --user pip
RUN pip3 install rasa
# RUN rasa init

COPY models ./models
COPY actions ./actions
COPY config.yml ./config.yml
COPY endpoints.yml ./endpoints.yml
COPY run.sh ./run.sh
COPY credentials.yml ./credentials.yml

EXPOSE 5005
EXPOSE 5055

CMD ["sh", "./run.sh"]
# sudo docker build -t rasa-chatbot-ampere-test-test .
# docker exec -it 274f92cd8f3a /bin/bash
# docker run -p 5005:5005 -p 5055:5055 rasa-chatbot-ampere-test-test