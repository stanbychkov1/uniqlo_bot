import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, \
    MessageHandler, filters
from dotenv import load_dotenv

from services import uniqlo_prices

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='I am a uniqlo bot, please give a '
                                        'product article to me!')


async def uniqlo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    res = uniqlo_prices(update.message.text)
    if type(res) == str:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=res)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=str(res[0]))
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=str(res[1]))


if __name__ == '__main__':
    application = ApplicationBuilder().token(
        os.getenv('TOKEN_TELEGRAM')).build()

    start_handler = CommandHandler('start', start)
    uniqlo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), uniqlo)

    application.add_handler(start_handler)
    application.add_handler(uniqlo_handler)

    application.run_polling()
