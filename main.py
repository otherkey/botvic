import os
import random
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# 🔑 Твой токен и Chat ID
TOKEN = "7364635550:AAEAA5XoarKX5jlsrtMAC3hChG6WVyAGetg"
#os.environ.get("TOKEN")
#это когда будет настроен токен и бот будет на сервере
CHAT_ID = -1002670681889  # ← твой chat_id из группы

bot = Bot(token=TOKEN)

#кусок ниже пишет токен айди при получении сообщения в группе
#async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    chat_id = update.effective_chat.id
#    print(f"Chat ID: {chat_id}")
#
#app = ApplicationBuilder().token(TOKEN).build()
#
# Любое сообщение
#app.add_handler(MessageHandler(filters.ALL, get_chat_id))
#
#app.run_polling()


# Переменная, куда будем сохранять
text_to_post = ""
buttons = []

async def handle_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global text_to_post

    full_text = update.message.text

    # Убираем только "/mypost " в начале
    user_input = full_text[len("/mypost "):] if full_text.startswith("/mypost ") else ""

    if user_input.strip():
        text_to_post = user_input
        await update.message.reply_text("Текст сохранён")
    else:
        await update.message.reply_text("Пожалуйста, добавь текст после /mypost")


async def handle_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    global buttons
    user_input = update.message.text[len("/myadd "):]

    # Убираем только "/mypost " в начале
    full_text = update.message.text
    user_input = full_text[len("/myadd "):] if full_text.startswith("/myadd ") else ""


    if user_input.strip():
        buttons.append([InlineKeyboardButton(user_input, callback_data=user_input)])
        await update.message.reply_text(f"Кнопка «{user_input}» добавлена")
    else:
        await update.message.reply_text("Пожалуйста, добавь текст кнопки после /myadd")


async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # нужно для "анимации нажатия"

    user = query.from_user
    data = query.data  # ← это то, что ты указала как callback_data

    # Пример: сохраняем, кто нажал и что
    print(f"{user.first_name} нажал кнопку: {data}")

async def handle_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global text_to_post
    if buttons:
        keyboard = InlineKeyboardMarkup(buttons)
        await context.bot.send_message(chat_id=CHAT_ID, text=text_to_post, reply_markup=keyboard)
    else:
        await context.bot.send_message(chat_id=CHAT_ID, text=text_to_post)    

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("mypost", handle_post))
app.add_handler(CommandHandler("mysend", handle_send))
app.add_handler(CommandHandler("myadd", handle_add))
app.add_handler(CallbackQueryHandler(handle_button_click))

app.run_polling()