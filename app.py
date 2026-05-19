from asyncio import tasks

from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta
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
    # Load environment variables
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    NOTION_TOKEN = os.getenv("NOTION_TOKEN")
    DATABASE_ID = os.getenv("DATABASE_ID")
    ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID"))

    # Helper functions
    def is_authorized(user_id):
      return user_id == ALLOWED_USER_ID
    
    def send_text(chat_id, text):
      url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
      payload = {
          "chat_id": chat_id,
          "text": text
      }
      requests.post(url, json=payload)

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
                        "text": "📊 View Records",
                        "callback_data": "view"
                    }
                ]
            ]
        }
    }

      requests.post(url, json=payload)

    def send_fillup_message(chat_id):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = get_today_tasks()
        results = data["results"]
        if not results:
            send_text(chat_id, "No task page found for today.")
            return
        page = results[0]
        properties = page["properties"]
        buttons = []
        for name, value in properties.items():
          if value["type"] == "checkbox":
              if value["checkbox"] == False:
                  buttons.append([
                      {
                          "text": f"☐ {name}",
                          "callback_data": name
                      }
                  ])
        payload = {
        "chat_id": chat_id,
        "text": "📝 Incomplete Tasks:",
        "reply_markup": {
            "inline_keyboard": buttons
          }
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
    
    def get_today_tasks():
        today = datetime.now().strftime("%Y-%m-%d")
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        headers = {
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        payload = {
            "filter": {
                "property": "Dates",
                "date": {
                    "equals": today
                }
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        print(data)
        return data
    
    def mark_task_complete(task_name):
        data = get_today_tasks()
        results = data["results"]
        if not results:
            return
        page = results[0]
        page_id = page["id"]
        url = f"https://api.notion.com/v1/pages/{page_id}"
        headers = {
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        payload = {
            "properties": {
                task_name: {
                    "checkbox": True
                }
            }
        }
        response = requests.patch(url, headers=headers, json=payload)
        print(response.json())
    
    def show_date_buttons(chat_id):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        buttons = []
        #Calculate the last 7 dates
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            buttons.append([
                {
                    "text": date,
                    "callback_data": f"date_{date}"
                }
            ])
        payload = {
        "chat_id": chat_id,
        "text": "📅 Select a date:",
        "reply_markup": {
            "inline_keyboard": buttons
          }
        }
        requests.post(url, json=payload)
    
    def selected_date_tasks(chat_id, date):
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        headers = {
              "Authorization": f"Bearer {NOTION_TOKEN}",
              "Content-Type": "application/json",
              "Notion-Version": "2022-06-28"
          }
        payload = {
              "filter": {
                  "property": "Dates",
                  "date": {
                      "equals": date
                  }
              }
        }
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        results = data["results"]
        if not results:
            send_text(chat_id, "No task page found for today.")
            return
        page = results[0]
        properties = page["properties"]
        message = f"📅 Tasks for {date}:\n\n"

        for name, value in properties.items():
            if value["type"] == "checkbox":
                status = "✅ Done" if value["checkbox"] else "❌ Not Done"
                message += f"{status} — {name}\n"

        send_text(chat_id, message)

    def get_today_checked_tasks(chat_id):
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = get_today_tasks()
        results = data["results"]
        if not results:
            return []
        page = results[0]
        properties = page["properties"]
        buttons = []
        for name, value in properties.items():
            if value["type"] == "checkbox" and value["checkbox"] == True:
                buttons.append([
                    {
                        "text": f"✅ {name}",
                        "callback_data": f"swap_{name}"
                    }
                ])
        payload = {
        "chat_id": chat_id,
        "text": "✅ Completed Tasks:",
        "reply_markup": {
            "inline_keyboard": buttons
          }
        }
        requests.post(url, json=payload)

    def swap_task_status(chat_id, task_name):
        data = get_today_tasks()
        results = data["results"]
        if not results:
            return
        page = results[0]
        page_id = page["id"]
        properties = page["properties"]
        current_status = None
        for name, value in properties.items():
            if name == task_name and value["type"] == "checkbox":
                current_status = value["checkbox"]
                break
        if current_status is None:
            return
        url = f"https://api.notion.com/v1/pages/{page_id}"
        headers = {
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        payload = {
            "properties": {
                task_name: {
                    "checkbox": not current_status
                }
            }
        }
        response = requests.patch(url, headers=headers, json=payload)
        print(response.json())

    #Extract Data from Telegram Webhook
    data = request.json
    print(data)
    message = data.get("message")
    callback_query = data.get("callback_query")

    #Message Handling
    if message:
        user_id = message["from"]["id"]
        chat_id = message["chat"]["id"]
        if not is_authorized(user_id):
            send_text(chat_id, "🚫 Access denied.")
            return "ok"
        text = message.get("text")
        if text == "/start":
            send_message(chat_id)
        else:
            send_text(chat_id, "Please type /start to interact with the bot.")

    if callback_query:
        user_id = callback_query["from"]["id"]
        chat_id = callback_query["message"]["chat"]["id"]

        if not is_authorized(user_id):
            send_text(chat_id, "🚫 Access denied.")
            return "ok"
        
        callback_data = callback_query["data"]
        chat_id = callback_query["message"]["chat"]["id"]
        print("Button clicked:", callback_data)
        if callback_data == "fillup":
            send_fillup_message(chat_id)
        elif callback_data == "edit":
            send_edit_message(chat_id)
            get_today_checked_tasks(chat_id)
        elif callback_data == "view":
            send_view_message(chat_id)
            show_date_buttons(chat_id)
        elif callback_data.startswith("date_"):
            selected_date = callback_data.split("_")[1]
            selected_date_tasks(chat_id, selected_date)
            send_message(chat_id)
        elif callback_data.startswith("swap"):
            selected_task = callback_data.split("_")[1]
            swap_task_status(chat_id, selected_task)
            send_message(chat_id)
        else:
          mark_task_complete(callback_data)
          send_message(chat_id)
        
    # Always return 200 OK to Telegram
    return "ok"

# @app.route("/generate", methods=["POST"])
# def generate():

#     body = request.json

#     print(body)

#     return jsonify(body)

if __name__ == "__main__":
    app.run(debug=True)