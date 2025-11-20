import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ناخذ المفتاح من متغيرات البيئة على Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-1.5-flash-latest:generateContent"
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/gemini", methods=["POST"])
def api_gemini():
    """
    هذا هو الـ API الذي تستدعيه دالة callGemini في index.html
    يأخذ prompt من الواجهة ويرسله إلى Gemini ويعيد نفس الرد JSON.
    """
    try:
        if not GEMINI_API_KEY:
            return jsonify(
                {"error": "MISSING_API_KEY", "message": "GEMINI_API_KEY is not set"}
            ), 500

        data = request.get_json() or {}
        prompt = data.get("prompt", "").strip()

        if not prompt:
            return jsonify({"error": "EMPTY_PROMPT"}), 400

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}],
                }
            ]
        }

        # نرسل الطلب إلى Gemini
        resp = requests.post(
            GEMINI_URL,
            params={"key": GEMINI_API_KEY},
            json=payload,
            timeout=40,
        )

        if resp.status_code != 200:
            # لو في خطأ من Google نرجّعه للواجهة عشان نفهم السبب
            return jsonify(
                {
                    "error": "UPSTREAM_ERROR",
                    "status": resp.status_code,
                    "body": resp.text,
                }
            ), 500

        # نعيد الـ JSON كما هو للواجهة
        return jsonify(resp.json())

    except Exception as e:
        # لو صار أي استثناء على السيرفر
        return jsonify(
            {"error": "SERVER_EXCEPTION", "message": str(e)}
        ), 500


if __name__ == "__main__":
    # تشغيل محلي فقط، على Render يستخدمون gunicorn app:app
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
