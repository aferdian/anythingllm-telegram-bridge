import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# MultiBots will inject these dynamically per bot
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ANYTHINGLLM_API_KEY = os.getenv("ANYTHINGLLM_API_KEY")
WORKSPACE_SLUG = os.getenv("WORKSPACE_SLUG")

ANYTHINGLLM_URL = f"https://allm.amazingmalang.net/api/v1/workspace/{WORKSPACE_SLUG}/chat"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Connected to the Knowledge Base. Ask me anything.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id) 
    headers = {
        "Authorization": f"Bearer {ANYTHINGLLM_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "message": update.message.text,
        "mode": "chat",
        "sessionId": user_id
    }
    
    try:
        response = requests.post(ANYTHINGLLM_URL, json=payload, headers=headers)
        data = response.json()
        bot_reply = data.get("textResponse", "Empty response.")
        await update.message.reply_text(bot_reply)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("System error: Could not reach the Knowledge Base.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print(f"Starting bot for workspace: {WORKSPACE_SLUG}")
    app.run_polling()
