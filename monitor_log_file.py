import subprocess
import json
import websocket
import time
import threading
import re



def send_message_to_django(message):
    ws = websocket.WebSocket()
    ws.connect("ws://127.0.0.1:8082/ws/chatbot-model/training/statistics/")  # WebSocket server address in Django
    ws.send(message)
    ws.close()


def monitor_log_file(log_file):
    # Open log file in read mode
    with open(log_file, 'r') as f:
        # Get the current file position
        f.seek(0, 2)  # Go to the end of the file

        # Continuously monitor the log file
        while True:
            # Read new lines added to the file
            line = f.readline()
            if line:
                # Send the line through the WebSocket
                send_message_to_django(line)  # Sneds all the lines
            else:
                # Sleep for a short interval before checking for new lines again
                time.sleep(1)


# # NOT WORKING
# def monitor_log_file(log_file):
#     # Open log file in read mode
#     with open(log_file, 'r') as f:
#         # Continuously monitor the log file
#         while True:
#             # Use tail command to get new lines added to the file
#             tail_process = subprocess.Popen(['tail', '-f', log_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#             # Read new lines from the tail process
#             for line in tail_process.stdout:
#                 # Strip leading and trailing whitespace characters (including newlines)
#                 # cleaned_line = line.decode().strip()
#                 # send_message_to_django(cleaned_line)
#                 # Extract epoch value using regular expression
#                 epoch_match = re.search(r'Epoch: (\d+)', line.decode('utf-8'))
#                 if epoch_match:
#                     epoch_value = epoch_match.group(1)
#                     # Send WebSocket message
#                     send_message_to_django(epoch_value)


# # Interpreting newline characters incorrectly
# def monitor_log_file(log_file):
#     # Open log file in read mode
#     with open(log_file, 'r') as f:
#         # Continuously monitor the log file
#         while True:
#             # Use tail command to get new lines added to the file
#             tail_process = subprocess.Popen(['tail', '-f', log_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#             # Read new lines from the tail process
#             for line in tail_process.stdout:
#                 send_message_to_django(line)


if __name__ == "__main__":
    log_file_path = "/media/robin/Documents/PersonalWorks/ibas_project/ibas-chatbot/train_log.txt"
    monitor_log_file(log_file_path)