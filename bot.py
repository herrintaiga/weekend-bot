import os
import telebot
from telebot import types

TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)

CITY_PLACES = [
    "Парк Горького",
    "Музей современного искусства",
    "Кофейня на Патриарших",
    "Новая Третьяковка"
]

COUNTRY_PLACES = {
    "близко": ["Парк усадьбы (30 мин)", "Озеро Лесное (20 мин)"],
    "средне": ["Усадьба Деда Мороза (1.5 часа)", "Горнолыжный склон (2 часа)"],
    "далеко": ["Заповедник (3+ часа)", "Старинный городок (4 часа)"]
}


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🏙 Город")
    btn2 = types.KeyboardButton("🌳 Загород")
    markup.add(btn1, btn2)
    return markup


def distance_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("До 30 минут", callback_data="dist_близко")
    btn2 = types.InlineKeyboardButton("1-2 часа", callback_data="dist_средне")
    btn3 = types.InlineKeyboardButton("2+ часа", callback_data="dist_далеко")
    markup.add(btn1, btn2, btn3)
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}! 👋\nКуда хотим на выходных?",
        reply_markup=main_menu()
    )


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "🏙 Город":
        places = "\n".join([f"• {p}" for p in CITY_PLACES])
        bot.send_message(
            message.chat.id,
            f"Вот варианты в городе:\n\n{places}",
            reply_markup=main_menu()
        )
    elif message.text == "🌳 Загород":
        bot.send_message(
            message.chat.id,
            "Как далеко готовы поехать?",
            reply_markup=distance_menu()
        )


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data.startswith("dist_"):
        dist_key = call.data.replace("dist_", "")
        places = COUNTRY_PLACES.get(dist_key, [])
        if places:
            text = f"Варианты за городом ({dist_key}):\n\n"
            text += "\n".join([f"• {p}" for p in places])
        else:
            text = "Пока нет вариантов для этой дальности."
        bot.send_message(call.message.chat.id, text, reply_markup=main_menu())
        bot.answer_callback_query(call.id)


if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()
