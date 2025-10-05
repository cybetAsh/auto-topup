from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

ADMIN_ID = 7516373366  # <-- මෙතනට ඔයාගේ Telegram ID එක දාන්න

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛒 Order Top-Up", callback_data="order")],
    ]
    await update.message.reply_text("👋 Welcome to Garena Order Bot!\nඔබට top-up order එකක් දාන්න පුළුවන් පහතින් 👇", 
                                    reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "order":
        await query.message.reply_text("🆔 ඔබේ Game ID එක යවන්න:")
        context.user_data["awaiting_id"] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_id"):
        game_id = update.message.text
        context.user_data["game_id"] = game_id
        context.user_data["awaiting_id"] = False
        await update.message.reply_text("💎 ඔබට අවශ්‍ය Shell / Diamond ප්‍රමාණය?")
        context.user_data["awaiting_amount"] = True
    elif context.user_data.get("awaiting_amount"):
        amount = update.message.text
        game_id = context.user_data.get("game_id")
        await update.message.reply_text("✅ ඔබේ order එක ලබාගන්න ලැබුණා!\nAdmin විසින් confirm කළ පසු ඔබට message එකක් එවනු ඇත.")
        await context.bot.send_message(ADMIN_ID, f"📥 නව Order එකක්:\n🎮 Game ID: {game_id}\n💎 Amount: {amount}\n👤 User: @{update.message.from_user.username}")
        context.user_data.clear()

app = ApplicationBuilder().token("8231654180:AAF6XBs38A31wdXpsKtrJm9QVDV9n9G392s").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
