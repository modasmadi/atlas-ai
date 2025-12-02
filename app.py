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


def build_style_from_mode(mode: str) -> str:
    """
    يرجّع جملة أسلوب الكتابة حسب النمط:
    - turbo: ردود مختصرة وسريعة
    - deep: ردود مفصلة ومنظمة
    """
    mode = (mode or "turbo").lower()
    if mode == "deep":
        return (
            "أجب بإجابات مفصلة ومنظمة بعناوين فرعية ونقاط، "
            "واستخدم أمثلة عند الحاجة، وركّز على أن تكون الإجابة شاملة."
        )
    else:
        return (
            "أجب بإجابات مختصرة ومركزة وواضحة قدر الإمكان، "
            "بدون حشو زائد، مع توضيح الفكرة الأساسية بسرعة."
        )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    """
    شات نصّي عادي (بدون صور)
    يستقبل: { "message": "..." , "mode": "turbo" | "deep" }
    يرجع:   { "reply": "..." }
    """
    try:
        if not GEMINI_API_KEY:
            return jsonify({
                "error": "missing_key",
                "message": "GEMINI_API_KEY not set!"
            }), 500

        payload = request.get_json() or {}
        user_msg = (payload.get("message") or "").strip()
        mode = (payload.get("mode") or "turbo").lower()

        if not user_msg:
            return jsonify({"reply": "اكتب رسالة أولاً علشان أقدر أساعدك 😊"})

        style = build_style_from_mode(mode)

        system_prompt = (
            "أنت مساعد ذكي خاص بمحمود. "
            "تساعده في النوتات، الدراسة، تنظيم الوقت، وتحليل الملفات والصور، "
            "وتجيب دائماً بالعربية وبأسلوب ودود ومنظم.\n"
        )

        full_prompt = f"{system_prompt}{style}\n\nرسالة المستخدم:\n{user_msg}"

        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(full_prompt)

        reply_text = response.text or "تعذّر الحصول على رد من النموذج."

        return jsonify({"reply": reply_text})

    except Exception as e:
        print("Backend Error (chat):", str(e), flush=True)
        return jsonify({"error": "backend_exception", "message": str(e)}), 500


@app.route("/api/image_chat", methods=["POST"])
def api_image_chat():
    """
    شات مع صورة:
    يستقبل: { "message": "...اختياري...", "image": "<BASE64>", "mode": "turbo" | "deep" }
    يرجع:   { "reply": "..." }
    """
    try:
        if not GEMINI_API_KEY:
            return jsonify({
                "error": "missing_key",
                "message": "GEMINI_API_KEY not set!"
            }), 500

        payload = request.get_json() or {}
        user_msg = (payload.get("message") or "").strip()
        image_b64 = payload.get("image")
        mode = (payload.get("mode") or "turbo").lower()

        if not image_b64:
            return jsonify({
                "error": "no_image",
                "message": "No image data provided."
            }), 400

        style = build_style_from_mode(mode)

        # فك تشفير الصورة من Base64
        img_bytes = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(img_bytes))

        system_prompt = (
            "أنت مساعد ذكي خاص بمحمود. "
            "تحلل الصور (مثل صور المحاضرات، السلايدات، الملاحظات المكتوبة بخط اليد، إلخ) "
            "وتستخرج منها أهم المعلومات للنوتات، الدراسة أو الملفات.\n"
        )

        if not user_msg:
            user_msg = (
                "حلّل هذه الصورة بالتفصيل، واشرح ما تحتويه، "
                "ولو فيها نصوص اكتبه بالعربية في شكل منظم، "
                "ثم جهّز المحتوى بحيث يكون مناسباً لملف PDF أو Word."
            )

        full_instruction = f"{system_prompt}{style}\n\nتعليمات إضافية:\n{user_msg}"

        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content([full_instruction, image])

        reply_text = response.text or "تعذّر قراءة رد النموذج على الصورة."

        return jsonify({"reply": reply_text})

    except Exception as e:
        print("Backend Error (image_chat):", str(e), flush=True)
        return jsonify({"error": "backend_exception", "message": str(e)}), 500


if __name__ == "__main__":
    # للتجربة محلياً فقط
    app.run(host="0.0.0.0", port=5000)
