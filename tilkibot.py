from transformers import GPT2Tokenizer, GPT2LMHeadModel
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import torch

# Model ve tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Token
TOKEN = "7970936715:AAFxTplKNd-8Ijz-2JyJaaeh9SULV7VGU9g"

# Sohbet geçmişi
gecmis = []

# Start komutu
def baslat(update, context):
    update.message.reply_text("Merhaba! Ben 500tilki botuyum. Mesaj gönder, cevaplayayım!")

# Metinlere yanıt
def cevapla(update, context):
    mesaj = update.message.text
    gecmis.append(f"Kullanıcı: {mesaj}")
    giris = "\n".join(gecmis[-5:])

    input_ids = tokenizer.encode(giris, return_tensors="pt")
    output = model.generate(input_ids, max_length=200, do_sample=True, top_k=50)
    yanit = tokenizer.decode(output[0], skip_special_tokens=True)
    cevap = yanit.replace(giris, "").strip()

    gecmis.append(f"Bot: {cevap}")
    update.message.reply_text(cevap)

# Botu başlat
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", baslat))  # /start komutu
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, cevapla))  # Diğer mesajlar

updater.start_polling()
updater.idle()
