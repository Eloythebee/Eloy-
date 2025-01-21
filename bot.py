import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import requests

# اطلاعات API
TELEGRAM_BOT_TOKEN = "7566908034:AAEXCWVWC_r1c4tbtbQd7K2qt6KcYZmShqE"
GENIUS_ACCESS_TOKEN = "04gaYI3MDTs0ZcTaOndIgUZtXjSfk417Y68Bqso8CqIIBsHpBkMI5iYItfka41h1"

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! Send the song name and artist to receive the lyrics.")

def get_lyrics(query):
    url = f"https://api.genius.com/search"
    headers = {"Authorization": f"Bearer {GENIUS_ACCESS_TOKEN}"}
    params = {"q": query}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        hits = response.json()["response"]["hits"]
        if hits:
            lyrics_url = hits[0]["result"]["url"]
            return lyrics_url
    return "متأسفم، متن آهنگ یافت نشد."

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_query = update.message.text
    logging.info(f"جستجوی آهنگ: {user_query}")

    lyrics_link = get_lyrics(user_query)
    await update.message.reply_text(lyrics_link)

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("ربات در حال اجراست...")
    app.run_polling()

if __name__ == "__main__":
    main()