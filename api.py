from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import main
app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/command', methods=['POST'])
def command():
    command = request.json['command']
    if command == "SCROLL":
        main.scroll(-100)
    return jsonify({'message': 'success!'}), 200

def run_server_api():
    app.run(host='0.0.0.0', port=8000)


if __name__ == "__main__":
    run_server_api()
