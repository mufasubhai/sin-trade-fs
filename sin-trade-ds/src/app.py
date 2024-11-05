#!/usr/bin/env python3
from flask import Flask, request
from flask_cors import CORS
import os

app = Flask(__name__)
# update this to reference environment variable. 
CORS(app, origins=["http:127.0.0.1:5002", "https://sin-trade-be-51f29d2bbbde.herokuapp.com/"])
port = os.environ.get("PORT", 5004)

@app.route("/")


def main():
    return '{"status":200, "data": "you have made a successful call"}'

# @app.route("/login")


# def login()