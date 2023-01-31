import random
from flask import Flask, request
import datetime

app = Flask(__name__, static_folder="static_file")

users={}
chats={}

@app.route('/chat', methods=["POST"])
def chat():
    chat_id=1
    chats[chat_id]={
        "chat_id":chat_id,
        "messages":[]
    }
    return chats[chat_id]

@app.route('/users/add', methods=["POST"])
def add_user():
    body=request.get_json()
    name=body['name']
    user_id=int(random.random()*1000000000000000)
    users[user_id]={
        "user_id": user_id,
        "name": name
    }
    return users[user_id]

@app.route('/message', methods=["POST"])
def send_massage():
    body=request.get_json()
    chat_id=body["chat_id"]
    sender_id=body['sender_id']
    text=body['text']

    message={
        "chat_id":chat_id,
        "sender_id":sender_id,
        "text":text,
        "send_date":datetime.date.today()
    }

    chat=chats[chat_id]
    chat["messages"].append(message)

    return "your massage is sent"

@app.route('/chat/<chat_id>/messages')
def get_messages(chat_id):
    chat=chats[int(chat_id)]
    chat_messages=chat["messages"]
    messages=list(map(lambda m: {
        "sender": users[m["sender_id"]]["name"],
        "text":m["text"],
        "send_date":m["send_date"].isoformat()
    }, chat_messages))
    return messages

app.run(host= '0.0.0.0', port=8888)