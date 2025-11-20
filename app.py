import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# نقرأ المفتاح من متغيرات البيئة على Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()

GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-1.5-flash-latest:generateContent"
)


@app.route("/")
def index():
    # صفحة ATLAS الرئيسية
    return render_template("index.html")


@app.route("/api/gemini", methods=["POST"])
def api_gemini():
    """نقطة الاتصال التي يستعملها الجافاسكربت في الموقع /api/gemini"""
    try:
        data = request.get_json(force=True) or {}
        prompt = (data.get("prompt") or "").strip()

        if not prompt:
            return jsonify({"error": "no_prompt", "message": "لا يوجد نص مرسل."}), 400

        if not GEMINI_API_KEY:
            # لو المفتاح مش موجود على Render
            return (
                jsonify(
                    {
                        "error": "no_api_key",
                        "message": "مفتاح GEMINI_API_KEY غير موجود على السيرفر.",
                    }
                ),
                500,
            )

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}],
                }
            ]
        }

        # نرسل الطلب إلى Gemini
        res = requests.post(
            GEMINI_ENDPOINT,
            params={"key": GEMINI_API_KEY},
            json=payload,
            timeout=30,
        )

        # لو صار خطأ من Google
        if res.status_code != 200:
            print(
                "Gemini API error:",
                res.status_code,
                res.text,
                flush=True,
            )
            return (
                jsonify(
                    {
                        "error": "gemini_error",
                        "status": res.status_code,
                        "details": res.text,
                    }
                ),
                500,
            )

        data = res.json()
        text = ""

        try:
            text = (
                data.get("candidates", [])[0]
                .get("content", {})
                .get("parts", [])[0]
                .get("text", "")
            )
        except Exception:
            text = ""

        if not text:
            text = "لم أستطع توليد رد مناسب من Gemini."

        return jsonify({"text": text})

    except Exception as e:
        # أي خطأ في الباك إند نفسه
        print("Backend /api/gemini exception:", repr(e), flush=True)
        return (
            jsonify(
                {
                    "error": "backend_exception",
                    "message": str(e),
                }
            ),
            500,
        )


if __name__ == "__main__":
    # للتجربة محلياً فقط
    app.run(host="0.0.0.0", port=5000, debug=True)
