#до конца не работает

import telebot
from telebot import types

# Замените 'your_token' на ваш токен бота
TOKEN = '6708953536:AAHOykPXIJK2ZaIGB7rHGh5Pt0CchHE-bH0'
bot = telebot.TeleBot(TOKEN)

# Список ресторанов и их меню
restaurants = {
    "Ресторан 1": ["Борщ", "Пельмени", "Салат", "Суп"],
    "Ресторан 2": ["Пицца", "Суши", "Стейк", "Паста"],
    "Ресторан 3": ["Бургер", "Шаурма", "Картошка фри", "Сэндвич"]
}

# Очередь заказов и время ожидания
orders_queue = []
waiting_time = 0


@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item_btn1 = types.KeyboardButton('Блюда')
    item_btn2 = types.KeyboardButton('Рестораны')
    item_btn3 = types.KeyboardButton('Заказы')
    item_btn4 = types.KeyboardButton('Настройки')
    markup.add(item_btn1, item_btn2, item_btn3, item_btn4)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == 'Рестораны':
        bot.send_message(message.chat.id, "Список ресторанов:")
        for restaurant in restaurants:
            bot.send_message(message.chat.id, restaurant)
    elif message.text == 'Блюда':
        markup = types.ReplyKeyboardMarkup(row_width=2)
        for restaurant in restaurants:
            item_btn = types.KeyboardButton(restaurant)
            markup.add(item_btn)
        bot.send_message(message.chat.id, "Выберите ресторан:", reply_markup=markup)
    elif message.text == 'Заказы':
        if orders_queue:
            bot.send_message(message.chat.id, "Очередь заказов:")
            for order in orders_queue:
                bot.send_message(message.chat.id, order)
            bot.send_message(message.chat.id, f"Время ожидания: {waiting_time} мин")
        else:
            bot.send_message(message.chat.id, "Очередь заказов пуста")
    elif message.text == 'Настройки':
        bot.send_message(message.chat.id, "Настройки пока недоступны")
    elif message.text == 'Ресторан 1':
        bot.send_message(message.chat.id, "Меню ресторана")

@bot.message_handler(func=lambda message: message.text in restaurants.keys())
def handle_menu(message):
    restaurant = message.text
    menu = restaurants.get(restaurant)
    print(menu)
    bot.send_message(message.chat.id, f"Меню ресторана {restaurant}:")
    for item in menu:
        bot.send_message(message.chat.id, item)


bot.polling()