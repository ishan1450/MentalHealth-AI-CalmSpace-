from flask import Flask , request , jsonify, render_template,session
from bert_model import sentiment_analysis
from model import generate_response
import os
import json

app = Flask(__name__)
# app.secret_key = os.urandom(24)

CRISIS_KEYWORDS = [  "kill myself", "suicide", "end my life", "want to die",
    "hurt myself", "cut myself", "can't go on", "overdose", "jump off"]

prompt = [{"role":"system","content":("You are a Mental Health assistant.Answer like a friend. Users will always be Indian but dont always provide them helpline numbers,only when they ask for it. Do not use any other language other than english. Have a conversation with them as if you are a human so the users feel safe expressing their feelings to you. Your job is to help users struggling with mental health issues. Help users navigate their feelings. Respond empathetically to the user" )}]
crisis = False

def is_crisis_msg(text):
    return any(kw in text.lower() for kw in CRISIS_KEYWORDS)
    

@app.route("/")
def index():
    # session["chat_history"] = []
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/chat",methods=["POST"])
def chat():
    global crisis
    user_msg = request.json["message"]
    detect_mood = sentiment_analysis(user_msg)

    prompt.append({"role":"user","content":user_msg})
    # if "chat_history" not in session:
    #           session["chat_history"] = []
        
    # session["chat_history"].append({"role":"user","content":user_msg})
    # prompt = [{"role":"system","content":("You are a Mental Health assistant.Have a conversation with them as if you are a human so the users feel safe expressing their feelings to you. Your job is to help users struggling with mental health issues. Help users navigate their feelings. Respond empathetically to the user" )}]
    # if is_crisis_msg(user_msg):
    #     user_msg+=("crisis")
    # print(crisis)
    # if "crisis" in user_msg:
    if is_crisis_msg(user_msg) or crisis:
        crisis = True
        reply = ("🚨 I'm really sorry you're feeling this way. "
            "You're not alone. Please talk to someone you trust or call a mental health professional.\n\n"
            "**India Helpline:** 9152987821 or visit https://icallhelpline.org")
    # if is_crisis_msg(user_msg):
    #     reply = ("🚨 I'm really sorry you're feeling this way. "
    #         "You're not alone. Please talk to someone you trust or call a mental health professional.\n\n"
    #         "**India Helpline:** 9152987821 or visit https://icallhelpline.org")
        
    #     # session["chat_history"].append({"role": "assistant", "content": reply})
        # prompt.append({"role":"user","content":user_msg})
        prompt.append({"role":"assistant","content":reply})


    else:
        reply = generate_response(prompt)
        prompt.append({"role":"assistant","content":reply})

        # session["chat_history"].append({"role": "assistant", "content": reply})
    
    return jsonify({"reply":reply})

if __name__ == "__main__":
    app.run(debug=True)