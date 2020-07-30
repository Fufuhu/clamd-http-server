import socket
import struct
import contextlib
import os

from flask import Flask, jsonify, request

from werkzeug.datastructures import FileStorage

app = Flask(__name__)
# 16MBまでアップロード可能
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route('/', methods=['GET'])
def index():
    response = {
        "Message": "This is index page."
    }
    return jsonify(response)


@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return '''
        <html>
            <body>
                <form action="/upload" method="POST" enctype="multipart/form-data">
                  <input type="file" name="file"/>
                  <input type="submit" value="submit"/>
                </form>
            </body>
        </html>
        '''
    if request.method != 'POST':
        # POSTでなければ405 Method Not Allowedを返す。
        message = {
            "Message": "Method is invalid. Only POST is allowed."
        }
        return jsonify(message), 405

    uploaded = request.files.get('file')
    if uploaded is None:
        message = {
            "Message": "No file found"
        }, 400

    result = send(file=uploaded)

    response = {
        "Message": "{} is uploaded.".format(uploaded.filename),
        "Result": result
    }
    return jsonify(response), 200


CLAMD_SERVER = 'CLAMD_SERVER'
CLAMD_LISTENING_PORT = 'CLAMD_LISTENING_PORT'

INSTREAM_COMMAND = "nINSTREAM\n".encode()
CHUNK_SIZE = 1024


def send(file: FileStorage, host: str = None, port: int = None) -> str:
    print(file)

    if host is None:
        clamd_server = os.environ.get(CLAMD_SERVER, 'localhost')
        clamd_port = int(os.environ.get(CLAMD_LISTENING_PORT, 3310))
    else:
        clamd_server = host
        clamd_port = port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((clamd_server, clamd_port))
        s.send(INSTREAM_COMMAND)

        chunk = file.stream.read(CHUNK_SIZE)
        print(chunk)
        while len(chunk) > 0:
            size = struct.pack(b'!L', len(chunk))
            s.send(size + chunk)
            chunk = file.stream.read(CHUNK_SIZE)

        s.send(struct.pack(b'!L', 0))

        with contextlib.closing(s.makefile('rb')) as f:
            response = f.readline().decode('utf-8').strip()

        print(response)

    return response


if __name__ == '__main__':
    listening_port = os.environ.get("CLAMD_HTTP_SERVER_LISTENING_PORT", "5000")
    app.run(debug=True, host='0.0.0.0', port=int(listening_port))
