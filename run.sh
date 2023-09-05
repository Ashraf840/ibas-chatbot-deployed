# nohup rasa run --enable-api --cors "*" >> chatbot.log &
#!/bin/sh

nohup rasa run --enable-api --cors "*" -p 5005 >> chatbot.log &
nohup rasa run actions -p 5055 >> actions.log &
tail -f chatbot.log

