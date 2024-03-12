from flask import Flask, request, render_template
import os
import socket
from datetime import datetime
import time
import sys

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_local_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def create_timestamped_folder():
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_name = os.path.join(app.config['UPLOAD_FOLDER'], current_time)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files[]' not in request.files:
        return 'No file part'

    files = request.files.getlist('files[]')
    folder_path = create_timestamped_folder()

    for file in files:
        if file.filename == '':
            return 'No selected file'

        file.save(os.path.join(folder_path, file.filename))

    return 'Files uploaded successfully'

@app.route('/progress')
def progress():
    def generate():
        total = request.args.get('total', 1)
        for i in range(int(total)):
            yield "data:" + str(i) + "\n\n"
    return app.response_class(generate(), mimetype="text/event-stream")

if __name__ == '__main__':
    ip_address = get_local_ip()
    port = sys.argv[1] if len(sys.argv) > 1 else 5000
    print(f"Automatically determined IP address: {ip_address}")
    app.run(host=ip_address, port=int(port), debug=False, threaded=True)