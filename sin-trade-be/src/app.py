#!/usr/bin/env python3
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
# update this to reference environment variable. 
CORS(app, origins=["http://localhost:5173"])


print(__name__)
@app.route("/")


def main():
    return '{"status":200, "data": "this has been a success"}'