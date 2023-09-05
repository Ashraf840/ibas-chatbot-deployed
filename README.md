# rasa_chatbot

## Installation
- Initiate a python virtual environment.
	- python -m venv venv
- Activate the virtual environment.
	- source venv/bin/activate
- Install the required python libraries.
	- `pip install requirements.txt`
- Create a new model using the CMD below.
	- rasa train

## Dataset:
 File: Chatbot_Agrani DOER.xlsx

## Training:
1. Download the dataset file on the current directory
2. Run `python data_curator.py`
3. Run `rasa train`
## Testing
### Run the action server for curtom actions
`rasa run actions`
### Using a stanalone CLI
Run `rasa shell`
### Using a web UI
1. Run `rasa run --enable-api --cors "*"`
2. Open ui/test_ui.html to your browser
