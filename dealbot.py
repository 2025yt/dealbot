from flask import Flask, request
import telegram
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
AFFILIATE_TAG = os.getenv("AFFILIATE_TAG")

bot = telegram.Bot(token=BOT_TOKEN)
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text.startswith("/start"):
            bot.send_message(
                chat_id=chat_id,
                text="🤖 Bot is live!\nUse /post AmazonLink"
            )

        elif text.startswith("/post"):
            try:
                link = text.split(" ", 1)[1]
                final_link = f"{link}?tag={AFFILIATE_TAG}"
                bot.send_message(
                    chat_id=chat_id,
                    text=f"✅ Affiliate Link:\n{final_link}"
                )
            except:
                bot.send_message(chat_id=chat_id, text="❌ Use: /post AmazonLink")

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
