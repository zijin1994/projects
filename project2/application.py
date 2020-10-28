import os
import json

from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit
from models import *

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

#initialize user and keep track of all the channels.
channel_names=[]
channels = []
names = []
users = []
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user_name")
    if name not in names:
        names.append(name)
        u = User(name)
        users.append(u)
    return jsonify(channel_names)

@app.route("/create", methods=["POST"])
def create():
    name = request.form.get("channel_name")
    creater = request.form.get("channel_creater")
    c = Channel(name, creater)
    for user in users:
        if user.name == creater:
            user.create_channel(c)
    if name in channel_names:
        return jsonify({"success": False})

    channels.append(c)
    channel_names.append(name)
    return jsonify({"success": True, "name": name, "creater": creater})

@app.route("/create/<string:name>", methods=["POST"])
def channel_room(name):
    for channel in channels:
        if channel.name == name:
            c = channel
    space = list(c.message_history)
    return jsonify(space)

@socketio.on("submit message")
def message(data):
    message = data["message"]
    time = data["time"]
    creater = data["creater"]
    channel = data["channel"]
    m = Message(message, time, creater)
    m_str = str(m)
    for c in channels:
        if c.name == channel:
            c.send_message(m_str)
    emit("show message",{"message": m_str},broadcast=True)

@socketio.on("delete message")
def delete_message(data):
    m = data["message"]
    channel = data["channel"]
    m_str = str(m)

    for c in channels:
         if c.name == channel:
             for ms in c.message_history:
                 if ms == m:
                     c.message_history.remove(ms)
    emit("complete",{"responses": m_str}, broadcast=True)
