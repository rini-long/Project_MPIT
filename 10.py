import logging
import sqlite3
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Подключение к базе данных
conn = sqlite3.connect('chatbot.db')
c = conn.cursor()

# Создание таблиц для хранения данных
c.execute(''' 
CREATE TABLE IF NOT EXISTS feedback ( 
    user_id INTEGER, 
    message TEXT 
)''')
c.execute(''' 
CREATE TABLE IF NOT EXISTS logs ( 
    user_id INTEGER, 
    message TEXT 
)''')
conn.commit()

spis_ds = [
    ["Детский сад № 6 Березка"],
    ["Детский сад № 14 Медвежонок"],
    ["Детский сад № 13 Карлсон"],
    ["Детский сад № 2 Сардаана"],
    ["Детский сад № 4 Лукоморье"],
    ["Детский сад № 55"],
    ["Детский сад № 1 Оленёнок"],
    ["Детский сад № 11 Теремок"],
    ["Детский сад № 8 Чоппууска"],
    ["Детский сад № 12 Солнышко"],
    ["Назад"]
]

spis_sotr = [
        ["Воспитателю"],
        ["Заведующему"],
        ["Бухгалтеру"],
        ["Психологу"],
        ["Медсестре"],
        ["Логопеду"],
        ["Назад"]
    ]

detskiysad = None
flag_ds = False
flag_sotr = False
flag_sotr_1 = False
flag_back = False
regim = 0
async def menu_ds(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = spis_ds
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Выберите детский сад:', reply_markup=reply_markup)


async def menu_sotr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = spis_sotr
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Выберите сотрудника:', reply_markup=reply_markup)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Создание клавиатуры с кнопками
    print(11)
    keyboard = [
        ["📅 График работы", "📞 Контакты"],
        ["💬 Отзывы", "❓ Часто задаваемые вопросы"],
        ["📝 Задать вопрос","📃 Список садиков"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Добро пожаловать в чат-бот АН ДОО "Алмазик". Выберите опцию:',
                                    reply_markup=reply_markup)

async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        ["📅 График работы", "📞 Контакты"],
        ["💬 Отзывы", "❓ Часто задаваемые вопросы"],
        ["📝 Задать вопрос", "📃 Список садиков"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Добро пожаловать в чат-бот АН ДОО "Алмазик". Выберите опцию:',
                                    reply_markup=reply_markup)


async def director(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Вы выбрали обращение заведующему. Пожалуйста, сформулируйте вопрос и отправьте мне. Я доставлю ваше обращение заведующему.'
    )


async def mentor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Вы выбрали обращение воспитателю. Пожалуйста, сформулируйте вопрос и отправьте мне. Я доставлю ваше обращение воспитателю.'
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global application, regim, flag_ds, flag_sotr, flag_sotr_1, detskiysad, sotrudnik

    user_id = update.message.from_user.id
    message = update.message.text


    c.execute('INSERT INTO logs (user_id, message) VALUES (?, ?)', (user_id, message))
    conn.commit()
    print(message)
    if message == "Назад":
        flag_sotr=False
        flag_sotr_1=False
        flag_ds=False

        await back(update, context)
    elif message == "📅 График работы":
        await update.message.reply_text("Наши часы работы: с 8:00 до 18:00 с понедельника по пятницу.")
    elif message == "📞 Контакты":
        await update.message.reply_text("Вы можете связаться с нами по телефону: +7 (123) 456-78-90.")
    elif message == "💬 Отзывы":
        regim = 1
        await update.message.reply_text("Пожалуйста, оставьте ваш отзыв после нажатия на кнопку 'Отправить отзыв'.")
    elif message == "❓ Часто задаваемые вопросы":
        await update.message.reply_text("Часто задаваемые вопросы: 1. Как записаться? ссылка \n2. Как получить документы? ссылка")
    elif message == "📝 Задать вопрос":
        regim=2
        await update.message.reply_text("Пожалуйста, задайте ваш вопрос.")
    elif message == "📃 Список садиков":

        await menu_ds(update, context)

    else:


        for sad in spis_ds:
            print(sad, message)
            if message == sad[0]:
                flag_ds = True
                detskiysad = sad[0]

        for ss in spis_sotr:
            if message == ss[0]:
                flag_sotr = True
                flag_ds = False
                sotrudnik = ss[0]

        if flag_ds:
            await menu_sotr(update, context)
        elif flag_sotr:
            response = "Введите ваше сообщение "+message + ". А я передам адресату."
            flag_sotr = False
            flag_sotr_1 = True
            await update.message.reply_text(response)
        else:
            response = generate_response(message, update, context)
            await update.message.reply_text(response)



def generate_response(message: str, update=None, context=None) -> str:
    global flag_sotr_1
    # Пример обработки стандартных запросов
    message = message.lower()
    if flag_sotr_1:

        flag_sotr_1 = False
        return "Отлично! Я передам Ваше сообщение"

    else:
        if regim==1:
            return "Спасибо за отзыв, нам важно ваше мнение."
        elif regim==2:
            return "Спасибо за вопрос. Мы скоро ответим ответим на ваш вопрос. Если обращение касается конкретного садика, просьба выбрать Детский садик и нужного сотрудника."
        else:
            print(flag_ds, detskiysad)
            return "Извините, я не понимаю ваш запрос. Пожалуйста, попробуйте переформулировать."


async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    message = update.message.text

    # Сохранение отзыва
    c.execute('INSERT INTO feedback (user_id, message) VALUES (?, ?)', (user_id, message))
    conn.commit()

    await update.message.reply_text("Спасибо за ваш отзыв!")

def main() -> None:
    application = ApplicationBuilder().token("7818585370:AAGFx7hZ0AMJNbQ-XdT6bIC_zQ0TnnhzJWU").build()  # Замените YOUR_TOKEN_HERE на ваш токен
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("feedback", feedback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':  # Исправлено имя на __name__
    main()