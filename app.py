from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# مفتاح Gemini (ما رح نكتبه هنا عند الرفع، رح نخليه من متغيرات البيئة)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"


@app.route("/")
def index():
    # يرجّع صفحة ATLAS
    return render_template("index.html")


@app.route("/api/gemini", methods=["POST"])
def gemini():
    if not GEMINI_API_KEY:
        return jsonify({"error": "GEMINI_API_KEY is not set"}), 500

    data = request.get_json() or {}
    prompt = data.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "no prompt"}), 400

    try:
        resp = requests.post(
            GEMINI_URL,
            params={"key": GEMINI_API_KEY},
            json={
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": prompt}],
                    }
                ]
            },
            timeout=40,
        )
    except Exception as e:
        return jsonify({"error": f"request failed: {e}"}), 500

    return (resp.text, resp.status_code, {"Content-Type": "application/json"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
