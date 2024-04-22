# бот с инлайн меню

import telebot
from telebot import types

# Замените 'your_token' на ваш токен бота
#TOKEN = '6708953536:AAHOykPXIJK2ZaIGB7rHGh5Pt0CchHE-bH0'
bot = telebot.TeleBot('TOKEN')

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
    markup = types.InlineKeyboardMarkup(row_width=2)
    item_btn1 = types.InlineKeyboardButton('Блюда', callback_data='get_dishes')
    item_btn2 = types.InlineKeyboardButton('Рестораны', callback_data='get_restaurants')
    item_btn3 = types.InlineKeyboardButton('Заказы', callback_data='get_orders')
    item_btn4 = types.InlineKeyboardButton('Настройки', callback_data='settings')
    markup.add(item_btn1, item_btn2, item_btn3, item_btn4)
    bot.send_message(message.chat.id, 'Приветствует Вас, {0.first_name}, в службе заказа.''\nВыберите действие:'.format(message.from_user), reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == 'get_dishes':
        bot.send_message(call.message.chat.id, "Выберите ресторан:")
        markup = types.InlineKeyboardMarkup()
        for restaurant in restaurants:
            item_btn = types.InlineKeyboardButton(restaurant, callback_data=f'dishes_{restaurant}')
            markup.add(item_btn)
        bot.send_message(call.message.chat.id, "Выберите ресторан:", reply_markup=markup)
    elif call.data == 'get_restaurants':
        bot.send_message(call.message.chat.id, "Список ресторанов:")
        for restaurant in restaurants:
            bot.send_message(call.message.chat.id, restaurant)
    elif call.data == 'get_orders':
        if orders_queue:
            bot.send_message(call.message.chat.id, "Очередь заказов:")
            for order in orders_queue:
                bot.send_message(call.message.chat.id, order)
            bot.send_message(call.message.chat.id, f"Время ожидания: {waiting_time} мин")
        else:
            bot.send_message(call.message.chat.id, "Очередь заказов пуста")
    elif call.data == 'settings':
        bot.send_message(call.message.chat.id, "Настройки пока недоступны")

# Запускаем бота
bot.polling()