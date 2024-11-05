#!/usr/bin/env python3
from flask import Flask, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
from supabase import create_client, Client
import logging

load_dotenv()

app = Flask(__name__)
# update this to reference environment variable. 
CORS(app, origins=["http://localhost:5173", "http://localhost:4173", "https://sin-trade-fe-14d4ac402398.herokuapp.com/", "https://sin-trade-ds-7ca730853eba.herokuapp.com/", "http:127.0.0.1:5002"])
port = os.environ.get("PORT", 5002)

# initializing supabase instance
url: str = os.getenv("SUPABASE_URL") 
key: str = os.getenv("SUPABASE_KEY") 


try: 
    supabase: Client = create_client(url, key)
    logging("set up supabase")
except Exception as e:
    logging.error(f"Failed to connect to database: {e}")
    supabase = None

print(Client)
@app.route("/")


def main():
    return '{"status":200, "data": "this has been a success"}'

@app.route("/login")
def login():
    return "login route"
