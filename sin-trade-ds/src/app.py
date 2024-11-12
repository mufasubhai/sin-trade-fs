#!/usr/bin/env python3
from flask import Flask, request
from flask_cors import CORS
import os
import logging

app = Flask(__name__)
app.config.from_object('config.DataServiceConfig') 
CORS(app, origins=app.config["CORS_ORIGINS"].split(','))
environment : str= app.config["ENVIRONMENT"]


if environment == "development": 
    logging.basicConfig(level=logging.INFO)

logging.info(app.config)


@app.route("/")

def main():
    return '{"status":200, "data": "you have made a successful call"}'

# @app.route("/login")
# def login()