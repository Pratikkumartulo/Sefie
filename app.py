from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():

    body = request.json

    properties = body.get("properties_value", {})

    entry = body.get("entry", "Habit Report")
    date = body.get("date", "Unknown Date")

    telegram_message = f"🌱 Daily Habit Report — {entry}\n\n"

    html_message = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4;">

      <div style="max-width: 600px; margin: auto; background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">

        <h2 style="color: #333;">📊 Daily Habit Report</h2>

        <p style="font-size: 16px;">
          <strong>Date:</strong> {date}
        </p>

        <hr style="border: none; border-top: 1px solid #eee;" />

        <ul style="line-height: 2; font-size: 15px; padding-left: 20px;">
    """

    completed = 0
    total = 0

    for key, value in properties.items():

        if isinstance(value, bool):

            total += 1

            if value:
                status = "✅ Done"
                completed += 1
            else:
                status = "❌ Not Done"

            telegram_message += f"{status} — {key}\n"

            html_message += f"""
            <li>
            <strong>{status}</strong> — {key}
            </li>
            """

    percentage = round((completed / total) * 100, 1) if total > 0 else 0

    telegram_message += f"\n📈 Completion: {completed}/{total} ({percentage}%)"

    html_message += f"""
        </ul>

        <div style="margin-top:20px; padding:15px; background:#f9f9f9; border-radius:10px;">
          📈 Completion Rate: <strong>{completed}/{total} ({percentage}%)</strong>
        </div>

        <div style="margin-top:15px; padding:15px; background:#f0fff4; border-radius:10px;">
          🌱 Consistency matters more than perfection.
        </div>

      </div>
    </div>
    """

    return jsonify({
        "telegram_message": telegram_message,
        "html_message": html_message
    })

@app.route("/webhook", methods=["POST"])
def webhook():
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    NOTION_TOKEN = os.getenv("NOTION_TOKEN")
    DATABASE_ID = os.getenv("DATABASE_ID")

    def send_message(chat_id):
      url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

      payload = {
        "chat_id": chat_id,
        "text": "🌱 Personal Habit System\n\nChoose an option:",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "📝 Fill Up Today's Tasks",
                        "callback_data": "fillup"
                    }
                ],
                [
                    {
                        "text": "✏️ Edit Today's Tasks",
                        "callback_data": "edit"
                    }
                ],
                [
                    {
                        "text": "📊 View Previous Records",
                        "callback_data": "view"
                    }
                ]
            ]
        }
    }

      requests.post(url, json=payload)
    def send_fillup_message(chat_id):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": "📝 Fill Up Mode Activated"
        }

        requests.post(url, json=payload) 
    def send_edit_message(chat_id):

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": "✏️ Edit Mode Activated"
        }

        requests.post(url, json=payload)
    def send_view_message(chat_id):

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": "📊 View Mode Activated"
        }

        requests.post(url, json=payload)
    
    data = request.json
    print(data)

    message = data.get("message")
    callback_query = data.get("callback_query")

    if message:
        text = message.get("text")
        chat_id = message["chat"]["id"]
        if text == "/start":
            send_message(chat_id)

    if callback_query:
        callback_data = callback_query["data"]
        chat_id = callback_query["message"]["chat"]["id"]
        print("Button clicked:", callback_data)
        if callback_data == "fillup":
            send_fillup_message(chat_id)
        elif callback_data == "edit":
            send_edit_message(chat_id)
        elif callback_data == "view":
            send_view_message(chat_id)

    return "ok"

# @app.route("/generate", methods=["POST"])
# def generate():

#     body = request.json

#     print(body)

#     return jsonify(body)

if __name__ == "__main__":
    app.run(debug=True)