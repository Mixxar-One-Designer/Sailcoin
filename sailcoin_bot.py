import logging
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# Replace with your actual bot token
TOKEN = '6897920395:AAEl4SH-ZdkLdYwC8Ex9t7sp5jNhT2Ei2ws'
SAILCOIN_IMAGE_ID = 'sailcoin_moon.JPG'  # Replace with the actual file ID of your image
SAILCOIN_COMMUNITY_URL = 'https://t.me/salcoin_dot'  # Replace with the actual URL of your Sailcoin community
SAILCOIN_MINING_URL = 'https://sailcoin-mining.vercel.app/'  # Your GitHub Pages URL

# Initialize logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Database setup
conn = sqlite3.connect('sailcoin_users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, balance INTEGER)''')
conn.commit()

def get_user_balance(user_id):
    c.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    return result[0] if result else 0

def update_user_balance(user_id, balance):
    c.execute('INSERT OR REPLACE INTO users (user_id, balance) VALUES (?, ?)', (user_id, balance))
    conn.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_id = user.id

    # Initialize user balance in database if not exists
    if get_user_balance(user_id) == 0:
        update_user_balance(user_id, 0)

    balance = get_user_balance(user_id)
    keyboard = [
        [InlineKeyboardButton("Let's Go", url=SAILCOIN_MINING_URL)],
        [InlineKeyboardButton("Join Sailcoin Community", url=SAILCOIN_COMMUNITY_URL)],
        [InlineKeyboardButton("Referral Earning", callback_data='referral_earning')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = (
        f"Hello {user.first_name}, Welcome to Sailcoin\n"
        f"News: @salcoin_dot\n"
        f"Tap on the Sailcoin and watch your balance grow.\n\n"
        f"SLC: {balance}"
    )
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=SAILCOIN_IMAGE_ID,
        caption=message,
        reply_markup=reply_markup
    )
    logger.info(f"Sent welcome message to {user.first_name} ({user.id})")

async def referral_earning(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    referral_link = f"https://t.me/sailcoin_bot?start={user_id}"  # Replace with your bot's username
    await query.edit_message_text(text=f"Share this referral link with your friends: {referral_link}")
    logger.info(f"Sent referral link to user {user_id}")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    if query.data == 'referral_earning':
        await referral_earning(update, context)

def main() -> None:
    """Start the bot."""
    try:
        # Create the Application and pass it your bot's token.
        application = Application.builder().token(TOKEN).build()

        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CallbackQueryHandler(button))

        # Run the bot until you press Ctrl-C
        application.run_polling()
    except Exception as e:
        logger.error(f"Error in main function: {e}")

if __name__ == '__main__':
    main()