import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

# Configuration
BOT_TOKEN = "7582532677:AAG-l5IenKCZxlSmbNTzCSfr4wMHzI1DrNM"  # Your bot token
CHANNEL_USERNAME = "@your_channel"  # without the @
GROUP_USERNAME = "@your_group"      # without the @
TWITTER_USERNAME = "your_twitter"   # without the @

async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    welcome_message = (
        f"👋 Welcome {user.first_name} to our Airdrop Bot!\n\n"
        "To participate in the airdrop, please complete these simple steps:"
    )
    
    keyboard = [
        [InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME}")],
        [InlineKeyboardButton("Join Group", url=f"https://t.me/{GROUP_USERNAME}")],
        [InlineKeyboardButton("Follow Twitter", url=f"https://twitter.com/{TWITTER_USERNAME}")],
        [InlineKeyboardButton("I've Joined All ✅", callback_data="joined_all")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == "joined_all":
        await query.edit_message_text("🎉 Great! Now please send me your Solana wallet address to receive your 10 SOL airdrop!")
    elif query.data == "done":
        await query.edit_message_text("✅ All steps completed! Thank you for participating!")

async def handle_wallet(update: Update, context: CallbackContext) -> None:
    wallet_address = update.message.text.strip()
    
    # Very basic Solana address validation (44 chars)
    if len(wallet_address) >= 32 and len(wallet_address) <= 44:
        response = (
            "🎉 Congratulations! 10 SOL is on its way to your wallet!\n\n"
            f"Wallet: {wallet_address}\n"
            "Transaction will appear soon on Solana Explorer.\n\n"
            "Thank you for participating in our airdrop!"
        )
    else:
        response = "⚠️ That doesn't look like a valid Solana wallet address. Please try again."
    
    await update.message.reply_text(response)

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    application.run_polling()

if __name__ == "__main__":
    main()
