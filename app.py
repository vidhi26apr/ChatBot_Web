import json
import random
import datetime
from fuzzywuzzy import fuzz
from flask import Flask, render_template, request, jsonify

# -------------------------
# Your existing chatbot code
# -------------------------
with open("intents.json") as f:
    intents = json.load(f)

def chatbot_response(user_input):
    user_input = user_input.lower()

    # Handle date
    if "date" in user_input:
        return f"Today's date is {datetime.date.today()}"

    # Handle math safely
    try:
        if all(char.isdigit() or char in "+-*/.() " for char in user_input):
            return str(eval(user_input))
    except:
        pass

    # Fuzzy matching with intents
    best_match = None
    highest_score = 0
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            score = fuzz.ratio(user_input, pattern.lower())
            if score > highest_score:
                highest_score = score
                best_match = intent

    if highest_score > 70:
        return random.choice(best_match["responses"])
    else:
        return "I didn’t understand that. Can you rephrase?"

# -------------------------
# Flask web app
# -------------------------
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json.get("message")
    response = chatbot_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
