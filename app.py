import os
import base64
import io

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from PIL import Image

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# مفتاح Gemini من Environment (GEMINI_API_KEY)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# نستخدم نفس الموديل في كل الطلبات
MODEL_NAME = "gemini-2.5-flash"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    """
    شات نصّي عادي (بدون صور)
    يستقبل: { "message": "..." }
    يرجع:   { "reply": "..." }
    """
    try:
        if not GEMINI_API_KEY:
            return jsonify({"error": "missing_key",
                            "message": "GEMINI_API_KEY not set!"}), 500

        payload = request.get_json() or {}
        user_msg = (payload.get("message") or "").strip()

        if not user_msg:
            return jsonify({"reply": "اكتب رسالة أولاً علشان أقدر أساعدك 😊"})

        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(
            f"أنت مساعد ذكي خاص بمحمود. أجب بالعربية وبأسلوب مرتب:\n\n{user_msg}"
        )

        reply_text = response.text or "تعذّر الحصول على رد من النموذج."

        return jsonify({"reply": reply_text})

    except Exception as e:
        print("Backend Error (chat):", str(e), flush=True)
        return jsonify({"error": "backend_exception", "message": str(e)}), 500


@app.route("/api/image_chat", methods=["POST"])
def api_image_chat():
    """
    شات مع صورة:
    يستقبل: { "message": "...اختياري...", "image": "<BASE64>" }
    يرجع:   { "reply": "..." }
    """
    try:
        if not GEMINI_API_KEY:
            return jsonify({"error": "missing_key",
                            "message": "GEMINI_API_KEY not set!"}), 500

        payload = request.get_json() or {}
        user_msg = (payload.get("message") or "").strip()
        image_b64 = payload.get("image")

        if not image_b64:
            return jsonify({"error": "no_image",
                            "message": "No image data provided."}), 400

        # فك تشفير الصورة من Base64
        img_bytes = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(img_bytes))

        model = genai.GenerativeModel(MODEL_NAME)

        # لو ما كتب رسالة، نعطيه برومبت افتراضي
        if not user_msg:
            user_msg = (
                "حلّل هذه الصورة بالتفصيل، واشرح ما تحتويه، "
                "ولو فيها نصوص اكتبه بالعربية في شكل منظم. "
                "ولو ينفع جهّز المحتوى بحيث يكون مناسب لملف PDF أو Word."
            )

        response = model.generate_content([user_msg, image])

        reply_text = response.text or "تعذّر قراءة رد النموذج على الصورة."

        return jsonify({"reply": reply_text})

    except Exception as e:
        print("Backend Error (image_chat):", str(e), flush=True)
        return jsonify({"error": "backend_exception", "message": str(e)}), 500


if __name__ == "__main__":
    # للتجربة محلياً فقط
    app.run(host="0.0.0.0", port=5000)
