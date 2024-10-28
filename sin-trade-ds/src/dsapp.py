
from flask import Flask, request

app = Flask(__name__)
print(__name__)

@app.route("/")

def main():
    return '{"status":200, "data": "you have made a successful call"}'