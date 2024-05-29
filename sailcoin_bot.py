import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# Replace with your actual bot token
TOKEN = '6897920395:AAEl4SH-ZdkLdYwC8Ex9t7sp5jNhT2Ei2ws'
SAILCOIN_IMAGE_ID = 'sailcoin_moon.JPG'  # Replace with the actual file ID of your image
SAILCOIN_COMMUNITY_URL = 'https://t.me/salcoin_dot'  # Replace with the actual URL of your Sailcoin community

# User data (This should ideally be stored in a database)
user_data = {}

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message with buttons when the command /start is issued."""
    user = update.effective_user
    user_data[user.id] = {'balance': 0}  # Initialize user balance
    keyboard = [
        [InlineKeyboardButton("Let's Go", callback_data='start_mining')],
        [InlineKeyboardButton("Join Sailcoin Community", url=SAILCOIN_COMMUNITY_URL)],
        [InlineKeyboardButton("Referral Earning", callback_data='referral_earning')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = (
        f"Hello {user.first_name}, Welcome to Sailcoin\n"
        f"News: @salcoin_dot\n"
        f"Tap on Sailcoin and watch your balance grow.\n\n"
        f"SLC: 0"
    )
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=SAILCOIN_IMAGE_ID,
        caption=message,
        reply_markup=reply_markup
    )

async def start_mining(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Simulate the mining process and update the user's balance."""
    query = update.callback_query
    user_id = query.from_user.id
    user = query.from_user

    # Initialize mining session
    await query.answer()
    await query.edit_message_text(text="Starting mining...")

    # Simulate mining process
    for i in range(5):  # Simulate 5 steps of mining
        await asyncio.sleep(2)  # Wait 2 seconds to simulate mining time
        user_data[user_id]['balance'] += 1  # Increment balance

        # Update user with current balance
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Mining in progress... Current SLC balance: {user_data[user_id]['balance']}"
        )

    # Final message after mining is complete
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Mining completed! Final SLC balance: {user_data[user_id]['balance']}"
    )

async def referral_earning(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate and send referral link."""
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    referral_link = f"https://t.me/sailcoin_bot?start={user_id}"  # Replace with your bot's username
    await query.edit_message_text(text=f"Share this referral link with your friends: {referral_link}")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button clicks."""
    query = update.callback_query

    if query.data == 'start_mining':
        await start_mining(update, context)
    elif query.data == 'referral_earning':
        await referral_earning(update, context)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Run the bot until you press Ctrl-Cs
    application.run_polling()

if __name__ == '__main__':
    main()
