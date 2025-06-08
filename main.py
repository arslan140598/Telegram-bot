import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# Logging sozlamalari
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Muhitdan o'zgaruvchilarni olish
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_1 = os.getenv("CHANNEL_1")
CHANNEL_2 = os.getenv("CHANNEL_2")
YOUR_CODE = os.getenv("YOUR_CODE")

# Obuna tekshiruvchi funksiya
async def is_subscribed(user_id, channel, context):
    try:
        member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
        return member.status in ['member', 'creator', 'administrator']
    except:
        return False

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    sub1 = await is_subscribed(user.id, CHANNEL_1, context)
    sub2 = True
    if CHANNEL_2:
        sub2 = await is_subscribed(user.id, CHANNEL_2, context)

    if sub1 and sub2:
        await update.message.reply_text(f"✅ Tabriklaymiz! Siz ro'yxatdan o'tdingiz.\nSizning kodingiz: `{YOUR_CODE}`", parse_mode='Markdown')
    else:
        keyboard = [
            [InlineKeyboardButton("📢 Kanal 1", url=f"https://t.me/{CHANNEL_1.replace('@','')}")],
        ]
        if CHANNEL_2:
            keyboard.append([InlineKeyboardButton("📢 Kanal 2", url=f"https://t.me/{CHANNEL_2.replace('@','')}")])
        keyboard.append([InlineKeyboardButton("✅ A'zo bo'ldim", callback_data="check_subs")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "👋 Salom, botimizga xush kelibsiz!\n\nKodni olish uchun quyidagi kanallarga obuna bo'ling:",
            reply_markup=reply_markup
        )

# Tugma bosilganda tekshirish
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user

    sub1 = await is_subscribed(user.id, CHANNEL_1, context)
    sub2 = True
    if CHANNEL_2:
        sub2 = await is_subscribed(user.id, CHANNEL_2, context)

    if sub1 and sub2:
        await query.edit_message_text(f"✅ Obuna uchun rahmat!\nSizning kodingiz: `{YOUR_CODE}`", parse_mode='Markdown')
    else:
        await query.edit_message_text("❌ Obuna bo'lmagansiz. Iltimos, barcha kanallarga obuna bo'ling va yana urinib ko'ring.")

# Botni ishga tushurish
async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
