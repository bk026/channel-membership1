import os, logging, requests
from fastapi import FastAPI, Request, Response
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from utils import download_instagram_video

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@learntospeake_1"
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"

app = FastAPI()
application = Application.builder().token(BOT_TOKEN).build()
logging.basicConfig(level=logging.INFO)

async def is_user_joined(bot, user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False

async def start(update, context):
    user_id = update.message.from_user.id
    if not await is_user_joined(context.bot, user_id):
        await update.message.reply_text(f"⚠️ पहले हमारे Telegram चैनल {CHANNEL_USERNAME} को Join करें ताकि बोट चल सके।")
        return
    await update.message.reply_text("👋 Welcome! बस Instagram लिंक भेजो — मैं HD वीडियो डाउनलोड कर दूँगा।")

async def handle_instagram(update, context):
    user_id = update.message.from_user.id
    if not await is_user_joined(context.bot, user_id):
        await update.message.reply_text(f"⚠️ पहले हमारे Telegram चैनल {CHANNEL_USERNAME} को Join करें।")
        return

    url = update.message.text
    if "instagram.com" not in url:
        await update.message.reply_text("❌ कृपया valid Instagram लिंक भेजें।")
        return

    await update.message.reply_text("⏳ Downloading HD video... कृपया इंतजार करें...")

    video_file = download_instagram_video(url)
    if video_file:
        await update.message.reply_video(video=open(video_file, "rb"))
        os.remove(video_file)
    else:
        await update.message.reply_text("⚠️ वीडियो डाउनलोड नहीं हो सका।")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_instagram))

@app.post(WEBHOOK_PATH)
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return Response(status_code=200)

@app.on_event("startup")
async def on_startup():
    public_url = os.getenv("PUBLIC_URL")
    if public_url:
        webhook_url = f"{public_url}{WEBHOOK_PATH}"
        await application.bot.set_webhook(webhook_url)
        logging.info("✅ Webhook set to %s", webhook_url)
