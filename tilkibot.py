from transformers import GPT2Tokenizer, GPT2LMHeadModel
from telegram.ext import Updater, MessageHandler, Filters
import torch

# Model ve tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Telegram bot token (kendi tokeninle değiştirebilirsin)
TOKEN = "7970936715:AAFxTplKNd-8Ijz-2JyJaaeh9SULV7VGU9g"

# Sohbet geçmişi (isteğe göre sınırlı tutuluyor)
gecmis = []

def cevapla(update, context):
    mesaj = update.message.text
    gecmis.append(f"Kullanıcı: {mesaj}")
    giris = "\n".join(gecmis[-5:])  # Son 5 mesajı kullanıyoruz

    input_ids = tokenizer.encode(giris, return_tensors="pt")
    output = model.generate(input_ids, max_length=200, do_sample=True, top_k=50)
    yanit = tokenizer.decode(output[0], skip_special_tokens=True)
    cevap = yanit.replace(giris, "").strip()

    gecmis.append(f"Bot: {cevap}")
    update.message.reply_text(cevap)

# Telegram botu başlat
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, cevapla))
updater.start_polling()
updater.idle()
