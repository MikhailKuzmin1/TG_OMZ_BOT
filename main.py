import numpy as np
from telebot import types
import telebot
from parsinfo import parser_services, parser_manager
import sqlite3
from config import secrets, TECH_CHAT_ID


token = secrets.get('BOT_API_TOKEN')
bot=telebot.TeleBot(token)
name = None

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAJvaWWqOz-5j3LeseRoRRljHHZ8JRvGAAI4CwACTuSZSzKxR9LZT4zQNAQ')
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    WebApp = types.WebAppInfo('https://it.omz.ru/')
    button_site = types.KeyboardButton(text='Наш сайт', web_app=WebApp)
    button_mail = types.KeyboardButton(text='Связаться')
    button_directors = types.KeyboardButton(text='Руководство')
    button_service = types.KeyboardButton(text='Услуги')
    button_help = types.KeyboardButton(text='Оставить обращение')
    keyboard.add(button_site, button_mail, button_directors, button_service, button_help)
    bot.send_message(message.chat.id, 'Добро пожаловать! Мы ИТ - компания. Рады вас видеть!', reply_markup=keyboard)

def send_request(message):
    new_request = f'Новое сообщение с чата компании:\n{message.text}'
    bot.send_message(TECH_CHAT_ID, new_request)
    bot.send_message(message.chat.id, 'Мы получили ваше сообщение! В случае необходимости наши сотрудники с вами свяжутся.')

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Опишите проблему.')
    bot.register_next_step_handler(message, about)

def about(message):
    number = int(''.join(map(str,np.random.randint(0,9,6))))
    about_problem = message.text.strip()
    conn = sqlite3.connect('help.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS application (id INTEGER primary key, name varchar(50), about text(250), number INTEGER)')
    cur.execute("INSERT INTO application (name, about, number) VALUES('%s', '%s', '%s')" % (name, about_problem, number))
    conn.commit()
    cur.close()
    conn.close()
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Просмотреть обращение', callback_data='application'))
    bot.send_message(message.chat.id, f'Ваше обращение принято.\n Номер вашего обращения: {number}', reply_markup=markup)
    
    
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    bot.send_message(call.message.chat.id, 'Введите номер обращения')
    bot.register_next_step_handler(call.message, my_ticket)

def my_ticket(message):
    number = message.text.strip()
    conn = sqlite3.connect('help.sql')
    cur = conn.cursor()
    cur.execute("SELECT * FROM application where number = '%s'" % (number))
    application = cur.fetchall()
    info = ''
    for i in application:
        info += f'Номер вашего обращиения: {i[3]}\nИмя: {i[1]}\nОписание: {i[2]}'
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, info)

@bot.message_handler(content_types=['text'])
def choise_point(message):
    if message.text.lower() == 'связаться': 
        bot.send_message(message.chat.id, 'Оставьте свои отзывы или предложения. Для ответа укажите свои контактные данные.')
        bot.register_next_step_handler(message, send_request)
    if message.text.lower() == 'услуги': 
        bot.send_message(message.chat.id, parser_services())
    if message.text.lower() == 'руководство':
        url_photo = ['https://it.omz.ru/gallery_gen/8ffa73046773beb9e33857ca04f5d20a_fit.png', 
                     'https://it.omz.ru/gallery_gen/1d42f558a607cfe5316ef4bbf9d155cc_fit.jpg']
        bot.send_media_group(message.chat.id, [telebot.types.InputMediaPhoto(photo) for photo in url_photo])
        bot.send_message(message.chat.id, parser_manager())
    if message.text.lower() == 'оставить обращение':
        bot.send_message(message.chat.id, 'Введите ваше имя.')
        bot.register_next_step_handler(message, user_name)
       
        
if __name__ == '__main__':
    bot.infinity_polling()
