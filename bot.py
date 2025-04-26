
import os
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

main_menu = [["Получить совет"], ["Выбраться из ступора"], ["О боте"]]

advices = {
    "Работа и карьера": [
        "Иногда кажется, что дело в начальнике или в коллегах. Но бывает другое ощущение — что всё вроде бы нормально, а внутри пусто...",
        "Соцсети придумали ужасную игру: бесконечно сравнивать свою черновую жизнь с чужими отредактированными моментами..."
    ],
    "Деньги и финансы": [
        "Деньги часто становятся не просто цифрами в кошельке, а точкой боли...",
        "Это чувство тяжёлое. Потому что оно не всегда связано с реальными цифрами..."
    ],
    "Отношения": [
        "Бывает, что отношения становятся как старый свитер: вроде бы тёплый, но давно колючий...",
        "Иногда люди пересекают наши личные границы не потому, что плохие, а потому, что мы сами молчим..."
    ],
    "Самочувствие и усталость": [
        "Бывают дни, когда внутри всё как будто выключается. Нет злости, нет радости — только пустота и апатия...",
        "Иногда само слово 'надо' парализует сильнее, чем объём задачи..."
    ],
    "Быт и рутина": [
        "В интернете жизнь часто выглядит так: йога на рассвете, идеальный завтрак...",
        "Переезд — это как собирать всю свою жизнь в коробки..."
    ]
}

micro_ideas = [
    "Давай найдем интересный подкаст на вечер?",
    "Не хочешь придумать, чем займемся в выходные?",
    "Сделать мини-зарядку для осанки на 2 минуты",
    "Почитать пару страниц книги, просто для удовольствия",
    "Выпить тёплый чай и ничего не делать пять минут"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я здесь, чтобы иногда подкидывать тебе идеи, советы и просто быть рядом. Что хочешь сейчас?",
        reply_markup=ReplyKeyboardMarkup(main_menu, resize_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Получить совет":
        themes = [[theme] for theme in advices.keys()]
        await update.message.reply_text("Выбери тему:", reply_markup=ReplyKeyboardMarkup(themes, resize_keyboard=True))
    elif text in advices:
        advice = random.choice(advices[text])
        await update.message.reply_text(advice)
    elif text == "Выбраться из ступора":
        idea = random.choice(micro_ideas)
        await update.message.reply_text(idea)
    elif text == "О боте":
        await update.message.reply_text("Я — сосед, который иногда заглядывает с идеей или советом. Просто рядом, когда хочется чего-то нового.")
    else:
        await update.message.reply_text("Не понял(а) запрос. Выбери в меню.")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
