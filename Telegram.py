import telebot
import pickle

token = '5293969375:AAHdUu56GoAPnJxhYejv96ZdSCe1mg6kwvQ'
bot = telebot.TeleBot(token, threaded=True)
commands = {'/about': True, '/help': True, '/start': True, '/check': True}

model = loaded_model = pickle.load(open('model.sav', 'rb'))


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id,
                     'Привет!\n' +
                     'Этот бот помогает определить стоимость продажи автомобиля.\n' +
                     'Используйте команду /help, чтобы научиться работать с ботом')


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id,
                     'Команда /check оценивает автомобиль по введенным параметрам\n' +
                     'Команда /about показывает создателей бота')


@bot.message_handler(commands=['about'])
def about_command(message):
    bot.send_message(message.chat.id,
                     'Беб Бебович\n' +
                     'Поппи Поппевна\n' +
                     'Валек Валекович')\

@bot.message_handler(commands=['about'])
def check_command(message):
    # brand, year, state, country, condition=1, title_status, mileage, color


if __name__ == '__main__':
    bot.polling(none_stop=True)
