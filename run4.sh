# nohup rasa run --enable-api --cors "*" >> chatbot.log &
# nohup rasa run actions >> actions.log &
# tail -f chatbot.log
nohup rasa run --enable-api --cors "*" >> log.txt 2>&1
nohup rasa run actions >> actions.log &
tail -f chatbot.log