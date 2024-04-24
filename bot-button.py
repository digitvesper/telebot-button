#работает


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
restaurant_details = {"Описание", "Отзывы", "Рейтинг", "Блюда", "Галерея" }
choose_restaurant = ""

# Очередь заказов и время ожидания
orders_queue = []
waiting_time = 0

def main_menu_markup():
    markup = types.ReplyKeyboardMarkup(row_width=3)
    buttons = [types.KeyboardButton(text) for text in ['Рестораны', 'Заказы', 'Настройки']]
    markup.add(*buttons)
    return markup

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=main_menu_markup())

@bot.message_handler(func=lambda message: message.text == 'Главное меню')
def handle_main_menu(message):
    bot.send_message(message.chat.id, "Возвращаемся в главное меню:", reply_markup=main_menu_markup())

@bot.message_handler(func=lambda message: message.text == 'Рестораны')
def handle_restaurants(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add(types.KeyboardButton('Главное меню'))
    for restaurant in restaurants:
        item_btn = types.KeyboardButton(restaurant)
        markup.add(item_btn)
    bot.send_message(message.chat.id, "Выберите ресторан:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Блюда')
def handle_dishes(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    for restaurant in restaurants:
        item_btn = types.KeyboardButton(restaurant)
        markup.add(item_btn)
    markup.add(types.KeyboardButton('Главное меню'))
    bot.send_message(message.chat.id, "Выберите ресторан:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in restaurants.keys())
def handle_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add(types.KeyboardButton('Главное меню'))
    markup.add(types.KeyboardButton('Рестораны'))
    restaurant = message.text
    menu = restaurants.get(restaurant)
    choose_restaurant = message.text
    for details in restaurant_details:
        item_btn = types.KeyboardButton(choose_restaurant+'. '+details)
        markup.add(item_btn)
    menu_text = f"Вы выбрали {restaurant}.\nВыберите информацию о ресторане\n" # + '\n'.join(menu)
    bot.send_message(message.chat.id, menu_text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Заказы')
def handle_orders(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add(types.KeyboardButton('Главное меню'))
    if orders_queue:
        bot.send_message(message.chat.id, "Очередь заказов:")
        for order in orders_queue:
            bot.send_message(message.chat.id, order, reply_markup=markup)
        bot.send_message(message.chat.id, f"Время ожидания: {waiting_time} мин", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "У вас нет заказа.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Настройки')
def handle_settings(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add(types.KeyboardButton('Главное меню'))
    bot.send_message(message.chat.id, "Настройки пока недоступны", reply_markup=markup)


bot.polling()