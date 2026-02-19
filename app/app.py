from flask import Flask
import mysql.connector
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return "Two-tier DevOps app running 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)