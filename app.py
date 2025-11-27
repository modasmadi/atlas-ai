import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)

# السماح بالوصول من أي موقع (عشان ملف الـ HTML شغال من جهازك / من نتلفاي ..الخ)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# قراءة مفتاح OpenAI
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    try:
        if not OPENAI_API_KEY:
            return jsonify({"error": "missing_key", "message": "OPENAI_API_KEY not set!"}), 500

        payload = request.get_json() or {}
        user_msg = payload.get("message", "").strip()

        if not user_msg:
            return jsonify({"reply": "أرسل رسالة أولاً كي أستطيع مساعدتك 😊"})

        # استدعاء نموذج GPT-4o-mini
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي خاص بمحمود، تجاوب بالعربية بأسلوب ودود."},
                {"role": "user", "content": user_msg},
            ],
        )

        # الصيغة الصحيحة مع مكتبة openai الجديدة
        reply = response.choices[0].message.content

        return jsonify({"reply": reply})

    except Exception as e:
        print("Backend Error:", str(e), flush=True)
        return jsonify({"error": "backend_exception", "message": str(e)}), 500


if __name__ == "__main__":
    # للتجربة محلياً فقط
    app.run(host="0.0.0.0", port=5000)
