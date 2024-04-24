from flask import Flask, jsonify
import subprocess
import asyncio
import websockets
import json
import websocket
import time
import threading


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


@app.route('/train_automation', methods=['GET'])
def run_script():
    try:
        response_data = {'status': 'Training started'}

        # Send a dummy progress data
        # t = threading.Thread(target=progress())
        # t.start()
        SendProgressThread().start()

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