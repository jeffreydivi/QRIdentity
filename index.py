#!/usr/local/bin/python3
# Web server
from flask import Flask, render_template, request, Response, redirect, abort, send_file
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import uuid, subprocess, os, json, binascii, requests, sys, hashlib, base64
from urllib.parse import urlparse
from datetime import datetime
import hashlib  # testing

# Debug mode:
# - Enables federation with most clients (un-breaks the Actor to be a Person).
# - Enables the auto-solve endpoint.
debug = False

app = Flask(__name__)


# In-memory database.
database = {}


@app.route("/client")
def client():
    return render_template("client.html")

@app.route("/client_override")
def client2():
    return render_template("client.html")

@app.route("/server")
def server():
    return render_template("server.html")


@app.route("/enroll/<username>/", methods=["POST"])
def enroll(username):
    print(request.get_json())

    database[username] = request.json

    return request.json


@app.route("/list/", methods=["GET"])
def list():
    return database


@app.route("/sw.js", methods=["GET"])
def service_worker():
    return send_file("static/sw.js")


@app.errorhandler(404)
def not_found(e):
    return "404 not found :(", 404


@app.errorhandler(401)
def unsigned_err(e):
    return "Request not signed", 401


def create_app():
    return app


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
