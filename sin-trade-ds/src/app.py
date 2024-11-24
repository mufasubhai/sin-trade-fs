
from flask import Flask, request
import os

app = Flask(__name__)
print(__name__)
port = os.environ.get("PORT", 5002)


@app.route("/")

def main():
    return '{"status":200, "data": "you have made a successful call  -- and we have updated "}'
