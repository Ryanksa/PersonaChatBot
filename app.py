from flask import Flask
from flask import request
from markupsafe import escape
from chatbot import converse
import database

database.connect_to_db()

app = Flask(__name__)


@app.route("/api/chatbot/<id>", methods=["GET"])
def get_chatbot(id):
    chatbot = database.get_chatbot(escape(id))
    return {'id': chatbot[0], 'name': chatbot[1]}


@app.route("/api/chatbot/create", methods=["POST"])
def create_chatbot():
    id = request.json.get("id")
    name = request.json.get("name")
    database.create_chatbot(id, name)
    return ""


@app.route("/api/personality/<id>", methods=["GET"])
def get_personalities(id):
    bot_id = escape(id)
    personalities = database.get_persona(bot_id)
    return {
        'id': bot_id,
        'personalities': list(map(lambda p: p[2], personalities))
    }


@app.route("/api/personality/add", methods=["POST"])
def add_personality():
    bot_id = request.json.get("id")
    personality = request.json.get("personality")
    database.add_persona(bot_id, personality)
    return ""


@app.route("/api/dialogue/<id>", methods=["GET"])
def get_dialogue(id):
    bot_id = escape(id)
    dialogues = database.get_dialogue(bot_id)
    return {
        'id': bot_id,
        'dialogue': list(map(lambda d: d[2], dialogues))
    }


@app.route("/api/converse", methods=["POST"])
def converse_bot():
    bot_id = request.json.get("id")
    message = request.json.get("message")
    if not isinstance(message, str) or message == "":
        return ""

    database.add_dialogue(bot_id, message)
    dialogue = database.get_dialogue(bot_id)
    dialogue = list(map(lambda d: d[2], dialogue))

    persona = database.get_persona(bot_id)
    persona = list(map(lambda p: p[2], persona))

    response = converse(dialogue, persona)
    database.add_dialogue(bot_id, response)

    return response


if __name__ == "__main__":
    app.run(hosts="0.0.0.0", port=5000)
