from telegram import Update
from telegram.ext import (
    ApplicationBuilder, MessageHandler,
    ContextTypes, filters
)
from deep_translator import GoogleTranslator
from keep_alive import keep_alive
import nest_asyncio
import asyncio

# Token bot kamu
TOKEN = "7866917376:AAEKBqX22XuGmnSSsUQOM2QLw8o-pCqO-N0"

# Fungsi deteksi & translate
def auto_translate(text: str) -> str:
    try:
        # Deteksi otomatis, target ke lawan bahasa
        lang_id = GoogleTranslator(source='auto', target='id').translate(text)
        if lang_id.lower() != text.lower():
            return lang_id  # artinya aslinya Inggris → Indonesia
        else:
            return GoogleTranslator(source='auto', target='en').translate(text)  # artinya aslinya Indonesia → Inggris
    except Exception as e:
        print("❗ Error:", e)
        return None

# Fungsi saat pesan masuk
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        text = update.message.text
        translated = auto_translate(text)
        if translated and translated.lower() != text.lower():
            await update.message.reply_text(f"🌐 {translated}")

# Fungsi utama
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot aktif 24 jam...")
    await app.run_polling()

# Aktifkan server untuk Replit
keep_alive()

# Jalankan di event loop aman
nest_asyncio.apply()
asyncio.run(main())