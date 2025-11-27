import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)

# السماح للواجهة (HTML) تتصل من أي مكان
CORS(app, resources={r"/api/*": {"origins": "*"}})

# قراءة مفتاح Gemini من متغير البيئة
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


@app.route("/")
def index():
    # لو كنت حاط index.html داخل مجلد templates
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    try:
        if not GEMINI_API_KEY:
            return jsonify({
                "error": "missing_key",
                "message": "GEMINI_API_KEY not set!"
            }), 500

        payload = request.get_json() or {}
        user_msg = (payload.get("message") or "").strip()

        if not user_msg:
            return jsonify({"reply": "اكتب رسالة أولًا علشان أقدر أساعدك 😊"})

        # إنشاء نموذج Gemini 2.5 Flash
        model = genai.GenerativeModel("gemini-2.5-flash")

        # إرسال الرسالة للنموذج
        response = model.generate_content(user_msg)

        # نص الرد
        reply_text = response.text or "تعذر قراءة رد النموذج."

        return jsonify({"reply": reply_text})

    except Exception as e:
        print("Backend Error:", str(e), flush=True)
        return jsonify({
            "error": "backend_exception",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    # للتجربة محلياً فقط
    app.run(host="0.0.0.0", port=5000)
