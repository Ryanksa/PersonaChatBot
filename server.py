from flask import Flask
from flask import request
from chatbot import converse

app = Flask(__name__)

"""
Expects a json body like this:
{
  "dialog": ["Hi, how are you?", ...],
  "persona": ["I am kind and caring.", ...]
}
Returns a string that is the chat bot's response to the dialog
"""
@app.route("/api/converse", methods=['GET', 'POST'])
def converse_bot():
    dialog = request.json.get("dialog")
    persona = request.json.get("persona")
    if not isinstance(dialog, list) or len(dialog) == 0 or not isinstance(dialog[0], str):
        return ""
    
    msg = converse(dialog, persona)
    return msg
  

if __name__ == "__main__":
  app.run(hosts="0.0.0.0", port=5000)