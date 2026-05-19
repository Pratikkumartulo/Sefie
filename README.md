# 🌱 Sefie — Personal Habit Tracking Telegram Bot

Sefie is a private productivity and habit tracking assistant built using:

- Python
- Flask
- Telegram Bot API
- Notion API
- Render
- Webhooks
- Dynamic Inline Telegram Keyboards

The bot allows real-time interaction with a Notion habit database directly from Telegram.

---

# ✨ Features

## ✅ Fill Up Tasks
Shows only incomplete tasks dynamically from Notion.

Clicking a task:
- instantly marks it completed
- updates Notion live
- refreshes Telegram UI automatically

---

## ✏️ Edit Tasks
Shows only completed tasks.

Useful for:
- undoing mistakes
- unchecking accidentally completed habits

Clicking a task:
- toggles checkbox state
- updates Notion instantly
- refreshes UI dynamically

---

## 📊 View Previous Records
Users can:
- select previous dates
- view historical habit completion
- check consistency and progress

---

## 🔄 Real-Time Sync
The system uses:
- Telegram Webhooks
- Flask backend
- Notion API

for instant two-way synchronization.

---

# 🧠 Project Architecture

```text
Telegram Bot
      ↓
Webhook
      ↓
Flask Backend
      ↓
Notion API
      ↓
Notion Database
```

The project is designed dynamically:
- no hardcoded tasks
- no static buttons
- scalable structure

Any new checkbox added in Notion automatically appears in the Telegram bot.

---

# 🔐 Security

The bot uses Telegram user authorization.

Only approved Telegram user IDs can:
- access tasks
- update habits
- edit records
- view history

Unauthorized users receive:
```text
🚫 Access denied.
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
BOT_TOKEN=your_telegram_bot_token

NOTION_TOKEN=your_notion_access_token

DATABASE_ID=your_notion_database_id

ALLOWED_USER_ID=your_telegram_user_id
```

⚠️ Never upload `.env` publicly to GitHub.

Add this to `.gitignore`:

```gitignore
.env
```

---

# 🗂️ Required Notion Database Structure

This project depends on a specific Notion database design.

Required columns:

| Column | Type |
|---|---|
| Entry | Title |
| Dates | Date |
| Any Habit Column | Checkbox |

Example:

| Entry | Dates | Workout | Meditation | Reading |
|---|---|---|---|---|
| Day 1 | 2026-05-19 | ✅ | ❌ | ✅ |

---

# ⚙️ Setup Instructions

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Pratikkumartulo/Sefie.git
```

---

## 2️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Configure `.env`

Add:
- Telegram Bot Token
- Notion Token
- Database ID
- Allowed Telegram User ID

---

## 4️⃣ Create Telegram Bot

Using:
```text
@BotFather
```

Required steps:
- create bot
- set profile picture
- set description
- disable group joining
- configure commands

---

## 5️⃣ Configure Webhook

Example:

```bash
https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=<YOUR_RENDER_URL>/webhook
```

---

## 6️⃣ Run Flask App

```bash
python app.py
```

---

# 🚀 Deployment

Recommended deployment:
- Render

The project uses webhooks, so HTTPS hosting is required.

---

# 🧩 Technologies Used

- Python
- Flask
- Requests
- Telegram Bot API
- Notion API
- Render
- dotenv

---

# 📌 Important Notes

This bot was built primarily as:
- a personal productivity system
- a backend engineering learning project

The project is tightly coupled with:
- Notion database structure
- Telegram callback architecture
- dynamic checkbox handling

If you want to recreate it:
- you must configure your own APIs
- create your own Notion database
- set your own authorization rules

---

# 🌿 Future Improvements

Planned upgrades:
- streak system
- analytics dashboard
- charts & reports
- AI habit suggestions
- reminder system
- multi-user support
- voice interaction
- advanced calendar navigation

---

# 📜 Privacy Policy

This bot stores and accesses only the data available in the connected private Notion workspace.

No personal data is:
- sold
- shared
- distributed to third parties

The project is intended for personal use only.

---

# 👨‍💻 Developer

Built by Pratik Kumar as a personal automation and backend engineering project.