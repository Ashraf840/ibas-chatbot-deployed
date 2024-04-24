from flask import Flask, jsonify
import subprocess
import asyncio
import websockets
import json
import websocket
import time
import threading
import re


app = Flask(__name__)

def send_message_to_django(message):
    ws = websocket.WebSocket()
    ws.connect("ws://127.0.0.1:8082/ws/chatbot-model/training/statistics/")  # WebSocket server address in Django
    ws.send(message)
    ws.close()


def progress():
    for progress in range(0, 101):
        send_message_to_django(json.dumps(progress))
        time.sleep(.2)


class SendProgressThread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        progress()


def monitor_log_file(log_file):
    # Open log file in read mode
    with open(log_file, 'r') as f:
        # Continuously monitor the log file
        while True:
            # Use tail command to get new lines added to the file
            tail_process = subprocess.Popen(['tail', '-f', log_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Read new lines from the tail process
            for line in tail_process.stdout:
                print(line)
                # send_message_to_django(line)
                # # Extract epoch value using regular expression
                # epoch_match = re.search(r'Epoch: (\d+)', line.decode('utf-8'))
                # if epoch_match:
                #     epoch_value = epoch_match.group(1)
                #     # Send WebSocket message
                #     send_message("New epoch value: " + epoch_value)


class ShellScriptThread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        subprocess.run(['./run.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)


@app.route('/train_automation', methods=['GET'])
def run_script():
    try:
        response_data = {'status': 'Training started'}

        # Send a dummy progress data through websocket
        # t = threading.Thread(target=progress())
        # t.start()
        # SendProgressThread().start()  # OK; 

        ShellScriptThread().start()

        return jsonify(response_data)

        # Run the 'run.sh' script using subprocess
        result = subprocess.run(['./run.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # Get the output and error messages
        print("result: ",result)
        output = result.stdout.decode('utf-8')
        error = result.stderr.decode('utf-8')

        if result.returncode == 0:
            return jsonify({'status': 'success', 'output': output})
        else:
            return jsonify({'status': 'error', 'output': output, 'error': error}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

        

if __name__ == '__main__':
    app.run(debug=True, port=5010)
    # log_file_path = "/media/robin/Documents/PersonalWorks/ibas_project/ibas-chatbot/train_log.txt"
    # monitor_log_file(log_file_path)