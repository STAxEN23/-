import telebot
from config import TOKEN_BOT, list_of_currencies
from extensions import Convertor, APIException


bot = telebot.TeleBot(TOKEN_BOT)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Привет!\n"\
        "Доступные команды:\n"\
        "/help - Помощь\n"\
        "/info - Информация о программе и авторе\n"\
        "/values - Увидеть список доступных валют\n"\
        "Введите <конвертируемая валюта> <валюта, в которую конвертируем> <кол-во валюты>\n" \
        "Пример:\n" \
        "рубль доллар 5000\n"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['info'])
def values(message: telebot.types.Message):
    text = "Это тестовый бот, созданный в рамках домашнего задания Skillfactory C5\n"\
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for i in list_of_currencies.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split()
    values = list(map(str.lower, values))
    try:
        result = Convertor.get_price(values)
    except APIException as e:
        bot.reply_to(message, e)
    except Exception as e:
        bot.reply_to(message, e)
    else:
        text = f'{values[2]} {list_of_currencies[values[0]]} = {result} {list_of_currencies[values[1]]}'
        bot.reply_to(message, text)


bot.polling(none_stop=True, interval=2)
