from flask import Flask, render_template, request, jsonify
from google import genai
import os

app = Flask(__name__)

# Get Gemini API key from environment
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured.")

client = genai.Client(api_key=api_key)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({
            "answer": "Please type a question."
        })

    try:
        response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=user_message
        )

        answer = response.text

        return jsonify({
            "answer": answer
        })

    except Exception as error:
        print("Gemini error:", error)

        return jsonify({
            "answer": "Sorry, I couldn't generate an answer right now. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
