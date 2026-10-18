import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Получаем токен из настроек сервера
TOKEN = os.getenv("BOT_TOKEN")

def main_menu():
    keyboard = [
        [InlineKeyboardButton("📅 Запланировать пост", callback_data="schedule")],
        [InlineKeyboardButton("🤖 ИИ-помощник", callback_data="ai")],
        [InlineKeyboardButton("💡 Идеи для канала", callback_data="advice")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 **AQUD Assistant запущен!**\n\nВыберите нужную функцию:",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "schedule":
        text = "📅 **Планировщик постов**\n\nМодуль готов к работе! Введите текст поста."
    elif query.data == "ai":
        text = "🤖 **AQUD AI**\n\nОтправьте мне тему или мысль, и я напишу пост."
    elif query.data == "advice":
        text = "💡 **Идеи для канала**\n\nО чем написать сегодня: разбор частой ошибки или опрос."
    else:
        text = "Неизвестная команда."

    await query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Меню", callback_data="home")]]),
        parse_mode="Markdown"
    )

async def home_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("🚀 **AQUD Assistant**\n\nВыберите функцию:", reply_markup=main_menu(), parse_mode="Markdown")

def main():
    if not TOKEN:
        raise RuntimeError("Ошибка: BOT_TOKEN не найден в переменных окружения!")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(home_handler, pattern="^home$"))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот успешно запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
