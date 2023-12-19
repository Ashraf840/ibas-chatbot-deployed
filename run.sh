#!/bin/bash

# Run the Python script and capture its output
python3 final_curator.py >> curator_log.txt 2>&1
rasa train >> train_log.txt 2>&1
echo 'chiro@840' | sudo -S kill -9 $(sudo lsof -t -i:5005)
echo 'chiro@840' | sudo -S kill -9 $(sudo lsof -t -i:5055)
nohup rasa run --enable-api --cors "*" >> log.txt 2>&1
nohup rasa run actions >> actions.log &
tail -f chatbot.log