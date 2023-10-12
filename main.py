from telegram import Update, ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from config import TOKEN
from get_audio import *

BOOKS, AUDIOS = 0, 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    buttons = getMainButtons()
    await update.message.reply_text(f'Assalomu alaykum <b>{update.effective_user.first_name}</b> \n\nCreated by @abdul_rozzaq', reply_markup=ReplyKeyboardMarkup(
        buttons, input_field_placeholder="Kitobni tanlang", resize_keyboard=True
    ), parse_mode='HTML')

    return BOOKS


async def second(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    buttons = getMainButtons()
    await update.message.reply_text('Kitobni tanlang', reply_markup=ReplyKeyboardMarkup(
        buttons, input_field_placeholder="Kitobni tanlang", resize_keyboard=True
    ), parse_mode='HTML')

    return BOOKS


async def getAudios(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    buttons = getAudiosName(msg)

    context.user_data['dir'] = msg

    await update.message.reply_text(f'Audioni tanlang', reply_markup=ReplyKeyboardMarkup(
        buttons, input_field_placeholder="Audioni tanlang", resize_keyboard=True
    ))

    return AUDIOS


async def getAudio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    # buttons = getAudiosName(msg)

    print(context.user_data['dir'], msg)

    bot_message = await update.message.reply_text('<i>Audio yuklanmoqda ...</i>', parse_mode='HTML')

    await update.message.reply_audio(audio=os.path.join(path, context.user_data['dir'], msg))
    await bot_message.delete()




app = ApplicationBuilder().token(TOKEN).build()


conv_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", start),
    ],
    states={
        BOOKS: [
            MessageHandler(filters.TEXT & (~ filters.Regex(
                r'^(\/start)$') & ~ filters.Regex(r'^(🔝 Asosiy menyu)$')), getAudios),
        ],
        AUDIOS: [
            MessageHandler(filters.TEXT & (~ filters.Regex(
                r'^(\/start)$') & ~ filters.Regex(r'^(🔝 Asosiy menyu)$')), getAudio),
        ],
    },
    fallbacks=[
        CommandHandler('start', second),
        MessageHandler(filters.Regex(r'(🔝 Asosiy menyu)'), second)
    ]
)
app.add_handler(conv_handler)
app.run_polling(allowed_updates=Update.ALL_TYPES)

# MessageHandler(filters.TEXT & (~ filters.Regex(r'^(\/cancel)$') & ~ filters.Regex(r'^(🔝 Asosiy menyu)$')), questions),
