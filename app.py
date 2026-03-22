import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

load_dotenv()

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

SYSTEM_PROMPT = (
    "Eres un asistente útil, claro y profesional. "
    "Responde en español, salvo que el usuario pida otro idioma."
)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        if not GROQ_API_KEY:
            return jsonify({
                "error": "No se encontró la variable de entorno GROQ_API_KEY."
            }), 500

        data = request.get_json(silent=True) or {}
        user_message = (data.get("message") or "").strip()
        history = data.get("history", [])

        if not user_message:
            return jsonify({"error": "El mensaje está vacío."}), 400

        safe_history = []
        if isinstance(history, list):
            for item in history[-10:]:
                if (
                    isinstance(item, dict)
                    and item.get("role") in ["user", "assistant", "system"]
                    and isinstance(item.get("content"), str)
                ):
                    safe_history.append({
                        "role": item["role"],
                        "content": item["content"]
                    })

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(safe_history)
        messages.append({"role": "user", "content": user_message})

        payload = {
            "model": GROQ_MODEL,
            "messages": messages,
            "temperature": 0.4,
            "n": 1
        }

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )

        result = response.json()

        if response.status_code != 200:
            error_message = (
                result.get("error", {}).get("message")
                if isinstance(result, dict)
                else "Error al consultar Groq."
            )
            return jsonify({"error": error_message or "Error al consultar Groq."}), response.status_code

        reply = result["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except requests.exceptions.Timeout:
        return jsonify({"error": "La solicitud a Groq tardó demasiado."}), 504
    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)