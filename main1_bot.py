import json
import os
from telegram.ext import Application, CommandHandler

TOKEN = "7862533064:AAFJw0GRNglM8P8i0On0hV4DVxS5Mrr3q0Y"

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

def format_ayet(ayet):
    """ Kullanıcının girdiği ayet numarasını uygun formata çevirir. """
    ayet = ayet.strip()
    ayet = ayet.replace(".", ":")
    ayet = ayet.replace(",", ":")
    return ayet

async def start(update, context):
    await update.message.reply_text("Merhaba! Ayet meali için ayet numarası girin. Örnek: 2:255")

async def get_meal(update, context):
    ayet_num = format_ayet(" ".join(context.args))
    if ayet_num in meal_data:
        await update.message.reply_text(f"{ayet_num}: {meal_data[ayet_num]}")
    else:
        await update.message.reply_text("❌ Bu ayet bulunamadı.")

# Telegram botunu başlat
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ayet", get_meal))

print("🚀 Bot çalışıyor...")
app.run_polling()
