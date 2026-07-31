from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

with open("knowledge.md", "r", encoding="utf-8") as file:
    KNOWLEDGE = file.read()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/miguelchat")
def miguelchat():
    return render_template("miguelchat.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data.get("message", "")

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": f"""
You are MiguelChat, the AI portfolio assistant for Miguel Medina.

Use the following information to answer questions about Miguel.

{KNOWLEDGE}

Rules:

- Answer using only the information provided above.
- If the answer is not available, say you don't have that information.
- Never invent experience, projects, certifications, or skills.
- Keep responses professional, concise, and friendly.
"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    response = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        return jsonify({
            "reply": f"DeepSeek Error: {response.text}"
        })

    result = response.json()

    reply = result["choices"][0]["message"]["content"]

    return jsonify({
        "reply": reply
    })


if __name__ == "__main__":
    app.run(debug=True)