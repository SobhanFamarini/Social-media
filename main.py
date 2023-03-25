from flask import Flask, request, jsonify
from deta import Deta
import datetime
import random

deta = Deta('a0c9y5il_ZTSDsshQqdWaYb232gmndzumHRzBaqMQ')
db = deta.Base('simpleDB')

app = Flask(__name__, static_folder="static_file")

chats={}
chat_id=1
chats[chat_id]={
    "chat_id":chat_id,
    "messages":[]
}

@app.route('/')
def route():
    return app.send_static_file('sign_up.html')

@app.route('/main')
def chat():
    return app.send_static_file("index.html")

@app.route('/sign_in')
def login():
    return app.send_static_file('sign_in.html')

@app.route('/private')
def private():
    return app.send_static_file('private.html')

@app.route('/group')
def group():
    return app.send_static_file('private_chat.html')

@app.route('/users', methods=["POST"])
def create_user():
    body = request.get_json()
    name = body['name']
    email = body['email']
    password = body['password']
    user = db.put({
        "name": name,
        "email": email,
        "password": password,
    })
    return jsonify(user,201)

@app.route("/users/<key>")
def get_user(key):
    user = db.get(key)
    return user if user else jsonify({"error": "Not found"}, 404)

@app.route("/users/<key>", methods=["PUT"])
def update_user(key):
    user = db.put(request.json, key)
    return user

@app.route("/users/<key>", methods=["DELETE"])
def delete_user(key):
    db.delete(key)
    return jsonify({"status": "ok"}, 200)

@app.route("/chat/add" , methods=['POST'])
def add_chat():
    body=request.get_json()
    name=body['name']
    chat_id=int(random.random() * 10000000000000000)
    chats[chat_id]={
        'chat_id':chat_id,
        'name':name,
        'messages': []
    }
    return chats[chat_id]

@app.route('/find')
def find_chat():
    return chats

@app.route('/message', methods=["POST"])
def send_massage():
    body=request.get_json()
    chat_id=int(body["chat_id"])
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
        "text":m["text"],
        "send_date":m["send_date"].isoformat()
    }, chat_messages))
    return messages

app.run(host= '0.0.0.0', port=8888)