
from flask import Flask
from threading import Thread
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)

# ===================== KEEP ALIVE SERVER =====================
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ===================== BOT CODE =====================

MODEL, NAME, PHONE, ADDRESS, SIZE = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if args and args[0].lower() == "استفسار":
        await update.message.reply_text(
            "👋 أهلاً وسهلاً بيك نورتنا!\n"
            "حابب تستفسر عن أي قطعة؟ ✨\n"
            "من فضلك ابعت *موديل القطعة* وهنتواصل معاك بكل التفاصيل ✅",
            parse_mode="Markdown"
        )
        return ConversationHandler.END

    await update.message.reply_text(
        "👟 من فضلك أدخل *كود الموديل* اللي حابب تحجزه:",
        parse_mode="Markdown"
    )
    return MODEL

async def get_model(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['model'] = update.message.text
    await update.message.reply_text("📝 تمام! دلوقتي ادخل *اسمك بالكامل*:", parse_mode="Markdown")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("📞 رقم الموبايل:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    await update.message.reply_text("📍 العنوان:")
    return ADDRESS

async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['address'] = update.message.text
    await update.message.reply_text("📏 مقاس القطعة:")
    return SIZE

async def get_size(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['size'] = update.message.text

    data = context.user_data
    summary = (
        f"✅ تم تأكيد الحجز!\n\n"
        f"📦 *كود الموديل:* {data['model']}\n"
        f"👤 *الاسم:* {data['name']}\n"
        f"📞 *رقم الموبايل:* {data['phone']}\n"
        f"📍 *العنوان:* {data['address']}\n"
        f"📏 *المقاس:* {data['size']}"
    )
    await update.message.reply_text(summary, parse_mode="Markdown")
    await update.message.reply_text("🙏 شكرًا لثقتك بنا! تم تأكيد الحجز بنجاح 💌\nهنقوم بالتواصل معاك قريبًا لتأكيد الطلب ✨")

    owner_id = 7440632062
    await context.bot.send_message(chat_id=owner_id, text=f"📥 طلب جديد:\n\n{summary}", parse_mode="Markdown")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ تم إلغاء العملية.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "استفسار" in text:
        await update.message.reply_text(
            "👋 أهلاً وسهلاً بيك نورتنا!\n"
            "حابب تستفسر عن أي قطعة؟ ✨\n"
            "من فضلك ابعت *موديل القطعة* وهنتواصل معاك بكل التفاصيل ✅",
            parse_mode="Markdown"
        )

def main():
    keep_alive()  # تشغيل السيرفر الخلفي
    TOKEN = "7819671532:AAEPVAANVZLnENgpIQz0h2h0WD-zi8KL2io"
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MODEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_model)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
            SIZE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_size)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

    print("✅ البوت شغال ومستني العملاء...")
    app.run_polling()

if __name__ == "__main__":
    main()
