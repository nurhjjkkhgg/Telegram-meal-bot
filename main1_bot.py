import json
import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# ✅ Telegram Bot Token (Render'dan al)
TOKEN = os.getenv("TOKEN")  # Render'daki Environment Variable'dan alıyor
if not TOKEN:
    print("❌ HATA: Bot Token bulunamadı! Lütfen Render'da Environment Variable eklediğinizden emin olun.")
    exit(1)

print("✅ TOKEN DEĞERİ:", TOKEN)  # Debug için tokeni gösteriyoruz (Hata ayıklama için)

# ✅ JSON dosyasının adını belirle
json_path = "meal_complete (1).json"

# ✅ JSON'u oku
try:
    with open(json_path, "r", encoding="utf-8") as f:
        meal_data = json.load(f)
        print("✅ JSON dosyası başarıyla yüklendi!")
except FileNotFoundError:
    meal_data = {}
    print("❌ JSON dosyası bulunamadı! Lütfen dosyanın doğru yüklendiğinden emin olun.")
except json.JSONDecodeError:
    meal_data = {}
    print("❌ JSON dosyası bozuk veya yanlış formatta! Lütfen JSON'un geçerli olduğundan emin olun.")

# ✅ Ayet formatlama fonksiyonu
def format_ayet(ayet):
    ayet = ayet.strip()
    ayet = ayet.replace(".", ":").replace(",", ":")
    return ayet

# ✅ Telegram bot komutları
async def start(update: Update, context):
    await update.message.reply_text("📖 Merhaba! Ayet meali için ayet numarası girin. Örnek: 2:255")

async def get_meal(update: Update, context):
    ayet_num = format_ayet(" ".join(context.args))
    if ayet_num in meal_data:
        await update.message.reply_text(f"📖 {ayet_num}: {meal_data[ayet_num]}")
    else:
        await update.message.reply_text("❌ Bu ayet bulunamadı.")

# ✅ Telegram botunu başlat
bot_app = Application.builder().token(TOKEN).build()
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CommandHandler("ayet", get_meal))

# ✅ Flask Uygulaması (Render için)
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is running! 🚀"

# ✅ Botun Kesintisiz Çalışmasını Sağlayan Fonksiyon
def run_bot():
    print("🚀 Telegram Bot Başlatılıyor...")
    bot_app.run_polling(allowed_updates=Update.ALL_TYPES)

# ✅ Flask Sunucusunu ve Botu Aynı Anda Çalıştır
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    
    # Port bilgisini al, yoksa varsayılan olarak 10000 kullan
    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)
