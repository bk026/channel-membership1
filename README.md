# Instagram Downloader Telegram Bot

### Features
- Download Reels / Stories in HD quality
- Works only if user joined your Telegram channel (@learntospeake_1)
- Render.com deployment ready (FastAPI + Webhook)

---

### Deploy on Render

1. Push this code to GitHub
2. Go to [Render.com](https://render.com)
3. Create new **Web Service**
4. Connect your GitHub repo
5. Set Build Command:
   ```
   pip install -r requirements.txt
   ```
6. Set Start Command:
   ```
   gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT
   ```
7. Add Environment Variables:
   - `BOT_TOKEN` = Your Telegram BotFather token  
   - `PUBLIC_URL` = https://your-app-name.onrender.com
8. Deploy ✅
