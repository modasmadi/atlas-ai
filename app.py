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


def build_profile_prompt(profile: str) -> str:
    """
    برومبت أساسي يعتمد على نوع المستخدم / الوضع (Profile).
    القيم المتوقعة من الفرونت:
      - uni      : طالب جامعة 🎓
      - school   : طالب مدرسة / توجيهي 📘
      - it       : مبرمج / IT 💻
      - work     : موظف / إنتاجية 🗂️
      - english  : مساعد أسئلة إنجليزي 🇬🇧
      - math     : مساعد رياضيات ➗
    """
    p = (profile or "uni").lower()

    if p == "school":
        return (
            "أنت مساعد لطالب مدرسة/توجيهي. اشرح الدروس بالعربية بأسلوب مبسط جداً، "
            "مع أمثلة بسيطة، ويمكنك أيضاً تقديم أسئلة اختيار من متعدد مع الإجابات."
        )
    elif p == "it":
        return (
            "أنت مساعد لمبرمج أو طالب IT. تشرح الأكواد، الأخطاء، المفاهيم البرمجية "
            "والشبكات وقواعد البيانات، مع أمثلة عملية. استخدم العربية في الشرح، "
            "ويمكنك كتابة الأكواد بالإنجليزية."
        )
    elif p == "work":
        return (
            "أنت مساعد لموظف/إنتاجية. تساعد في تنظيم المهام، كتابة الإيميلات، "
            "تلخيص الاجتماعات، ووضع خطط عمل وجداول يومية وأسبوعية."
        )
    elif p == "english":
        return (
            "أنت مساعد لحل أسئلة اللغة الإنجليزية. تساعد في القواعد، المفردات، "
            "كتابة وترجمة الجمل، وحل الأسئلة، مع شرح بالعربية عند الحاجة. "
            "اعطِ الجواب بالإنجليزية متبوعاً بشرح بسيط بالعربية."
        )
    elif p == "math":
        return (
            "أنت مساعد رياضيات لجميع المراحل (مدرسية وجامعية). "
            "حل مسائل الرياضيات خطوة بخطوة، واشرح المنطق وراء كل خطوة بالعربية، "
            "ويمكنك استخدام رموز رياضية واضحة، وإذا كان السؤال من صورة فافترض أنه يحتوي "
            "على مسألة رياضيات أو تعبيرات عددية أو رموز، وحاول استخراجها وحلّها."
        )
    else:  # uni (طالب جامعة) كافتراضي
        return (
            "أنت مساعد لطالب جامعة. تركز على تلخيص المحاضرات والكتب، "
            "وشرح المفاهيم الجامعية، وتحضير نوتات للامتحانات، "
            "ويمكنك أيضاً اقتراح أسئلة وأجوبة للمراجعة."
        )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    """
    شات نصّي عادي (بدون صور)
    يستقبل: { "message": "..." , "mode": "turbo" | "deep", "profile": "uni|school|it|work|english|math" }
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
        profile = (payload.get("profile") or "uni").lower()

        if not user_msg:
            return jsonify({"reply": "اكتب رسالة أولاً علشان أقدر أساعدك 😊"})

        style_text = build_style_from_mode(mode)
        profile_text = build_profile_prompt(profile)

        system_prompt = (
            "أنت مساعد ذكاء اصطناعي خاص بالمستخدم محمود. "
            "تتكيف مع احتياجاته الدراسيّة والشخصية حسب نوع الملف الشخصي (Profile).\n\n"
            f"{profile_text}\n\n"
            f"{style_text}\n"
        )

        full_prompt = f"{system_prompt}\nرسالة المستخدم:\n{user_msg}"

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
    يستقبل: { "message": "...اختياري...", "image": "<BASE64>", "mode": "turbo" | "deep", "profile": "uni|school|it|work|english|math" }
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
        profile = (payload.get("profile") or "uni").lower()

        if not image_b64:
            return jsonify({
                "error": "no_image",
                "message": "No image data provided."
            }), 400

        style_text = build_style_from_mode(mode)
        profile_text = build_profile_prompt(profile)

        # فك تشفير الصورة من Base64
        img_bytes = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(img_bytes))

        base_system = (
            "أنت مساعد ذكاء اصطناعي خاص بمحمود. "
            "تستقبل صوراً (مثل صور المحاضرات، السلايدات، الملاحظات المكتوبة، أو مسائل الرياضيات والصور التعليمية) "
            "وتستخرج منها أهم المعلومات التي يحتاجها حسب نوع الملف الشخصي (Profile).\n\n"
        )

        if not user_msg:
            # في حال لم يرسل نصاً مع الصورة، نضع تعليمات افتراضية
            user_msg = (
                "حلّل هذه الصورة بالتفصيل، واشرح ما تحتويه، "
                "ولو فيها نصوص أو مسائل اكتبه بالعربية في شكل منظم، "
                "ثم جهّز المحتوى بحيث يكون مناسباً لملف PDF أو Word."
            )

        full_instruction = (
            base_system
            + profile_text + "\n\n"
            + style_text + "\n\n"
            + "تعليمات إضافية من المستخدم:\n"
            + user_msg
        )

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
