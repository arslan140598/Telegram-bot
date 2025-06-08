import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

CHANNELS = ["@your_channel1", "@your_channel2"]  # ← bu yerga o'zingizning kanallaringizni yozing
USER_CODE = "ABC-1234"  # foydalanuvchiga beriladigan kod

def check_subscription(user_id):
    for channel in CHANNELS:
        result = bot.get_chat_member(channel, user_id)
        if result.status in ['left', 'kicked']:
            return False
    return True

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    for ch in CHANNELS:
        markup.add(InlineKeyboardButton(text=f"➕ {ch}", url=f"https://t.me/{ch[1:]}"))
    markup.add(InlineKeyboardButton("✅ A'zo bo‘ldim", callback_data="check_subs"))
    text = "🎉 SALOM BIZNING BOTIMIZGA XUSH KELIBSIZ!\nKod olish uchun quyidagi kanallarga a'zo bo‘ling:"
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_subs")
def check_subs_callback(call):
    if check_subscription(call.from_user.id):
        bot.edit_message_text("✅ Obuna tasdiqlandi!", call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f"🎁 Sizning kodingiz: `{USER_CODE}`", parse_mode="Markdown")
    else:
        bot.answer_callback_query(call.id, "❗ Iltimos, barcha kanallarga a'zo bo‘ling.")

bot.infinity_polling()
