import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8559323592

WALLET = "TFcLisJ8jTNTBbTU2LoGC3Mo6AQ1UnzJw5"
CHANNEL_1 = "https://t.me/+m5tt78scF2RhODFk"
CHANNEL_2 = "https://t.me/+MHIdsX4IcysyODVk"
SUPPORT = "@Dr_7_Khaled"

users = set()


def menu():
    keyboard = [
        ["BOT 125X 🤖", "إحصائيات 📊", "قناة نتائج المشتركين"],
        ["مجموعة Vip", "قنوات Vip", "طرق الدفع 💳"],
        ["Forex ⭐", "قناة الوساطة لبيع وشراء usdt"],
        ["إعلان هام 📢‼️", "قناة الكورسات", "الاستراتيجية"],
        ["كورسات مجانًا", "أفضل منصة 💎"],
        ["القناة الرئيسية ❤️‍🔥", "مجانا القناة الخاصة"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.effective_user.id)
    await update.message.reply_text(
        "👑 أهلاً بك في بوت VIP الاحترافي\n\n"
        "اختر من القائمة:",
        reply_markup=menu()
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == "plans":
        await q.message.reply_text(
            "👑 باقات VIP\n\n"
            "✅ توصيات خاصة\n"
            "✅ نتائج ومتابعة\n"
            "✅ دخول القنوات الخاصة\n"
            "✅ دعم مباشر\n\n"
            "للاشتراك اضغط الدفع 💳"
        )

    elif data == "pay":
        await q.message.reply_text(
            f"💳 الدفع عبر USDT TRC20\n\n"
            f"المحفظة:\n`{WALLET}`\n\n"
            "بعد الدفع أرسل صورة التحويل.",
            parse_mode="Markdown"
        )

    elif data == "proof":
        await q.message.reply_text("📤 أرسل صورة إثبات الدفع الآن.")

    elif data == "results":
        await q.message.reply_text("📊 النتائج متاحة للمشتركين فقط.")

    elif data == "support":
        await q.message.reply_text(f"📞 الدعم: {SUPPORT}")

    elif data.startswith("ok_"):
        uid = int(data.split("_")[1])
        await context.bot.send_message(
            uid,
            f"✅ تم قبول اشتراكك!\n\n{CHANNEL_1}\n\n{CHANNEL_2}"
        )
        await q.message.reply_text("✅ تم قبول العميل.")

    elif data.startswith("no_"):
        uid = int(data.split("_")[1])
        await context.bot.send_message(uid, f"❌ تم رفض الدفع. تواصل مع الدعم {SUPPORT}")
        await q.message.reply_text("❌ تم رفض الطلب.")

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users.add(user.id)

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ قبول", callback_data=f"ok_{user.id}"),
        InlineKeyboardButton("❌ رفض", callback_data=f"no_{user.id}")
    ]])

    caption = (
        "📥 إثبات دفع جديد\n\n"
        f"👤 الاسم: {user.full_name}\n"
        f"🆔 ID: `{user.id}`\n"
        f"🔗 @{user.username if user.username else 'لا يوجد'}"
    )

    await context.bot.send_photo(
        ADMIN_ID,
        update.message.photo[-1].file_id,
        caption=caption,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

    await update.message.reply_text("✅ تم استلام إثبات الدفع، انتظر المراجعة.")

async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.effective_user.id)
    await update.message.reply_text("اختر من القائمة:", reply_markup=menu())

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.PHOTO, photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text))
    app.run_polling()

if __name__ == "__main__":
    main()
