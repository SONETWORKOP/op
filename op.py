import logging
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, CallbackContext
import requests

# User provided values
API_KEY = 'svKvhh0O4zGyUB6NisB7tfwUwb6uGUM1JALcUwLR'
EMAIL = 'ojhashivam81@gmail.com'
DOMAIN = 'shivamop.tech'
ZONE_ID = '3021220b0309ca795740ef2ad8adf35f'
BOT_TOKEN = '7206685163:AAF7cxUTxcKSzsryRmBBIB38Ge8WJQQavJk'

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(name)

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Welcome! Use /create <ip> <subdomain> to create a subdomain.')

async def create(update: Update, context: CallbackContext) -> None:
    try:
        ip = context.args[0]
        subdomain = context.args[1]
    except IndexError:
        await update.message.reply_text('Usage: /create <ip> <subdomain>')
        return

    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records"
    data = {
        "type": "A",
        "name": f"{subdomain}.{DOMAIN}",
        "content": ip,
        "ttl": 1,
        "proxied": False
    }
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Email": EMAIL,
        "X-Auth-Key": API_KEY
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        await update.message.reply_text(f"Subdomain created successfully: {subdomain}.{DOMAIN}")
    else:
        await update.message.reply_text(f"Failed to create subdomain: {subdomain}.{DOMAIN}. It might already exist.")

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("create", create))

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    application.run_polling()

if name == 'main':
    main(
