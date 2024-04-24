#!/bin/bash

# Run the Python script and capture its output
python3 final_curator.py >> curator_log.txt 2>&1  # Will uncomment after testing



# Start the model training & simultaneously write the training log file
rasa train >> train_log.txt 2>&1 &

python3 monitor_log_file.py
# # Kill any orphaned service of Rasa after the training is completed
# echo 'ashraf826546' | sudo -S kill -9 $(sudo lsof -t -i:5005)
# echo 'ashraf826546' | sudo -S kill -9 $(sudo lsof -t -i:5055)
# # Start the rasa model server & write logs
# nohup rasa run --enable-api --cors "*" >> log.txt 2>&1
# # Start the rasa action server & write logs
# nohup rasa run actions >> actions.log &
# tail -f chatbot.log