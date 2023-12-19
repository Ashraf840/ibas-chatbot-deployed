from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/train_automation', methods=['GET'])
def run_script():
    try:
        # response_data = {'status': 'Training started'}
        # return jsonify(response_data)

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
    app.run(debug=True)