from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f'Hello, this is your Python script running inside Docker! Current time: {current_time}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
