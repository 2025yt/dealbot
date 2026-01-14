from telegram.ext import Updater, CommandHandler
import requests
from bs4 import BeautifulSoup
import re

# =========================
# CONFIG
# =========================
import os
BOT_TOKEN = os.getenv("8289591348:AAFIsZ1zgzyBbfyMozYF9GXmi3hjvQzVj64")
CHANNEL_USERNAME = os.getenv("@Loot_Deals_2026")
AFFILIATE_TAG = os.getenv("lootdeal0b9-21")
# =========================
# POST FUNCTION
# =========================
def post(update, context):
    if not context.args:
        update.message.reply_text("Use: /post AmazonLink")
        return

    url = context.args[0]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    r = requests.get(url, headers=headers, allow_redirects=True)
    soup = BeautifulSoup(r.text, "html.parser")

    title_tag = soup.select_one("#productTitle")
    title = title_tag.text.strip() if title_tag else "Product"

    price_tag = soup.select_one("span.a-price-whole")
    deal_price = price_tag.text.replace(",", "").strip() if price_tag else None

    mrp_tag = soup.select_one("span.a-text-price span.a-offscreen")
    mrp_price = mrp_tag.text.replace("₹", "").replace(",", "").strip() if mrp_tag else None

    discount = ""
    if deal_price and mrp_price:
        try:
            discount_percent = round(
                (int(mrp_price) - int(deal_price)) / int(mrp_price) * 100
            )
            discount = f"📉 Discount: {discount_percent}% OFF"
        except:
            discount = ""

    image_tag = soup.select_one("#imgTagWrapperId img")
    image_url = image_tag["src"] if image_tag else None

    url = re.sub(r"[?&]tag=[^&]+", "", url)
    if "?" in url:
        url += "&tag=" + AFFILIATE_TAG
    else:
        url += "?tag=" + AFFILIATE_TAG

    caption = f"""🔥 Deal Alert 🔥

📦 {title}

💰 Deal Price: ₹{deal_price if deal_price else "Check Link"}
🏷️ MRP: ₹{mrp_price if mrp_price else "Check Link"}
{discount}

👉 Buy Now: {url}

⚡ Limited Time Offer
"""

    if image_url:
        context.bot.send_photo(
            chat_id=CHANNEL_USERNAME,
            photo=image_url,
            caption=caption
        )
    else:
        context.bot.send_message(
            chat_id=CHANNEL_USERNAME,
            text=caption
        )

    update.message.reply_text("✅ Deal posted with image & discount")

# =========================
# BOT START (MOST IMPORTANT)
# =========================
updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("post", post))

updater.start_polling()
print("🤖 Bot is running...")
updater.idle()

