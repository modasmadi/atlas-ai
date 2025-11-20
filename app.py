import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Read Gemini API key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()

# MODEL + ENDPOINT (correct one)
GEMINI_MODEL = "gemini-1.5-flash-latest"
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/gemini", methods=["POST"])
def api_gemini():
    try:
        payload = request.get_json()
        prompt = payload.get("prompt", "")

        if not GEMINI_API_KEY:
            return jsonify({"error": "missing_key", "message": "GEMINI_API_KEY not set!"}), 500

        data = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ]
        }

        res = requests.post(
            GEMINI_ENDPOINT,
            params={"key": GEMINI_API_KEY},
            json=data,
            timeout=30
        )

        if res.status_code != 200:
            print("Gemini ERROR:", res.text, flush=True)
            return jsonify({"error": "gemini_error", "details": res.text}), 500

        r = res.json()

        text = (
            r.get("candidates", [])[0]
             .get("content", {})
             .get("parts", [])[0]
             .get("text", "")
        )

        return jsonify({"text": text})

    except Exception as e:
        print("Backend Error:", str(e), flush=True)
        return jsonify({"error": "backend_exception", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
