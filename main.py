import telebot
from telebot import types

TOKEN = '6727634551:AAH64-c35sywIFOwb0kAjxMXrmlk2Kb5d3s'
bot = telebot.TeleBot(TOKEN)
books = [
    {'name': 'Hunger Games', 'price': 1590, 'description': 'A thrilling adventure novel.', 'picture': 'https://cdn.miridei.com/files/img/c/idei-dosuga/kakuyu-knigu-pochitat/8_157.jpg'},
    {'name': 'Twilight', 'price': 2190, 'description': 'A romantic fantasy novel.', 'picture': 'https://d1466nnw0ex81e.cloudfront.net/n_iv/600/1154335.jpg'}
]

def send_info(chat_id, book):
    # Создаем кнопки для цены и описания
    button_price = types.InlineKeyboardButton('Price', callback_data=f'price')
    button_description = types.InlineKeyboardButton('Description', callback_data=f'description')
    
    # Создаем разметку с этими кнопками
    markup = types.InlineKeyboardMarkup().row(button_price, button_description)

    # Отправляем сообщение с информацией о книге и разметкой
    bot.send_message(chat_id, 'Info about the book ', reply_markup=markup)
    bot.send_photo(chat_id, book['picture'])


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'What book are you looking for?')

@bot.message_handler(func=lambda message: True)
def text(message):
    
    global chosen_book
    find_book = message.text
    chosen_book=find_book
    for book in books:
        if find_book.lower() == book['name'].lower():
            send_info(message.chat.id, book)
            break
    else:
        bot.send_message(message.chat.id, 'Book not found. Please try again.')
        

@bot.callback_query_handler(func=lambda call: call.data == 'price')
def handle_price_callback(call):
    global chosen_book
    chat_id = call.message.chat.id

    for book in books:
        if book['name'] == chosen_book:
            price=book['price']
            break
    
    bot.send_message(chat_id, f'The price is: {price}')

@bot.callback_query_handler(func=lambda call: call.data == 'description')
def handle_description_callback(call):
    global chosen_book
    chat_id = call.message.chat.id
    for book in books:
        if book['name'] == chosen_book:
            description=book['description']
            break

    bot.send_message(chat_id, f'Description: {description}')

bot.polling()