import json
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = "7862533064:AAFJw0GRNglM8P8i0On0hV4DVxS5Mrr3q0Y"

# JSON dosyasının yolunu belirle
json_path = os.path.expanduser("~/meal.json")

# JSON'u oku
try:
    with open(json_path, "r", encoding="utf-8") as f:
        meal_data = json.load(f)
        print("✅ JSON dosyası başarıyla yüklendi.")
except FileNotFoundError:
    meal_data = {}
    print("❌ JSON dosyası bulunamadı!")
except json.JSONDecodeError:
    meal_data = {}
    print("❌ JSON dosyası bozuk veya yanlış formatta!")

def format_ayet(ayet):
    """ Kullanıcının girdiği ayet numarasını JSON formatına uygun hale getir """
    ayet = ayet.strip()  # Başındaki ve sonundaki boşlukları temizle
    ayet = ayet.replace(".", ":")  # 2.255 → 2:255 dönüşümü
    ayet = ayet.replace(",", ":")  # 2,255 → 2:255 dönüşümü

    # Kullanıcı "Bakara 2:255" gibi yazarsa, sadece "2:255" kısmını al
    parts = ayet.split()
    if len(parts) > 1:
        ayet = parts[-1]

    # Kullanıcı sadece sure numarası yazdıysa, onu "1. ayet" olarak al
    if ayet.isdigit():
        ayet = f"{ayet}:1"

    # Debug için ekrana yazdıralım
    print(f"🔍 Aranan ayet: {ayet}")

    return ayet

def get_meal(ayet):
    formatted_ayet = format_ayet(ayet)
    return meal_data.get(formatted_ayet, f"❌ {formatted_ayet} ayeti bulunamadı.")

def meal(update: Update, context: CallbackContext):
    if context.args:
        ayet = " ".join(context.args)  # Eğer "Bakara 2:255" gibi yazarsa
        meal_text = get_meal(ayet)
        update.message.reply_text(meal_text)
    else:
        update.message.reply_text("📌 Lütfen bir ayet numarası girin. Örn: /meal 2:255")

# Telegram botunu başlat
updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler("meal", meal))

print("🚀 Bot başlatıldı...")
updater.start_polling()
updater.idle()