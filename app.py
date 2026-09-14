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


@app.route("/accounting")
def accounting():
    return render_template("accounting.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}

    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({
            "reply": "Please enter a question."
        }), 400

    if not DEEPSEEK_API_KEY:
        return jsonify({
            "reply": "The DeepSeek API key is not configured."
        }), 500

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

    try:
        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            return jsonify({
                "reply": f"DeepSeek Error: {response.text}"
            }), response.status_code

        result = response.json()

        reply = result["choices"][0]["message"]["content"]

        return jsonify({
            "reply": reply
        })

    except requests.RequestException:
        return jsonify({
            "reply": "MiguelChat could not connect to the AI service."
        }), 503

    except (KeyError, IndexError, TypeError):
        return jsonify({
            "reply": "MiguelChat received an unexpected response."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)