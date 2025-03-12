import json
import os
import threading
from flask import Flask
from telegram.ext import Application, CommandHandler

TOKEN = os.getenv("TOKEN")  # Render'daki Environment Variable'dan alıyor

# JSON dosyasının adını belirle
json_path = "meal.json"

# JSON'u oku
try:
    with open(json_path, "r", encoding="utf-8") as f:
        meal_data = json.load(f)
        print("✅ JSON dosyası başarıyla yüklendi!")
except FileNotFoundError:
    meal_data = {}
    print("❌ JSON dosyası bulunamadı!")
except json.JSONDecodeError:
    meal_data = {}
    print("❌ JSON dosyası bozuk veya yanlış formatta!")

# Ayet formatlama fonksiyonu
def format_ayet(ayet):
    ayet = ayet.strip()
    ayet = ayet.replace(".", ":").replace(",", ":")
    return ayet

# Telegram bot komutları
async def start(update, context):
    await update.message.reply_text("Merhaba! Ayet meali için ayet numarası girin. Örnek: 2:255")

async def get_meal(update, context):
    ayet_num = format_ayet(" ".join(context.args))
    if ayet_num in meal_data:
        await update.message.reply_text(f"{ayet_num}: {meal_data[ayet_num]}")
    else:
        await update.message.reply_text("❌ Bu ayet bulunamadı.")

# Telegram botunu başlat
bot_app = Application.builder().token(TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("ayet", get_meal))

# Flask Uygulaması
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# Botun Kesintisiz Çalışmasını Sağlayan Fonksiyon
def run_bot():
    print("🚀 Telegram Bot Başlatılıyor...")
    bot_app.run_polling()

# Flask Sunucusunu ve Botu Aynı Anda Çalıştır
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
