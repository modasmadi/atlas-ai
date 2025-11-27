import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# قراءة مفتاح OpenAI من Render
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()

# تهيئة عميل OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    try:
        payload = request.get_json()
        user_msg = payload.get("message", "")

        if not OPENAI_API_KEY:
            return jsonify({"error": "missing_key", "message": "OPENAI_API_KEY not set!"}), 500

        # اتصال بنموذج GPT-4o
        response = client.chat.completions.create(
            model="gpt-4o-mini",          # الأفضل والأخف والأسرع
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي لمحمود."},
                {"role": "user", "content": user_msg}
            ]
        )

        reply = response.choices[0].message["content"]

        return jsonify({"reply": reply})

    except Exception as e:
        print("Backend Error:", str(e), flush=True)
        return jsonify({"error": "backend_exception", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
