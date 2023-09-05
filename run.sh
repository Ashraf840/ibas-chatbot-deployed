nohup rasa run --enable-api --cors "*" >> chatbot.log &
nohup rasa run actions >> actions.log &
tail -f chatbot.log