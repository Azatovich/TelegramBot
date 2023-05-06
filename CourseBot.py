import telebot
from config import *
from extensions import Convertor, APIException


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start", "help"]) #Приветвие
def help(message: telebot.types.Message):
    text = "Чтобы начать работу введите комманду боту в следующем формате: \n<имя валюты> \
     <в какую валюту перевести> \
      <количество переводимой валюты> Увидеть список всех доступных валют: /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=["values"])# Список валют для конвертации
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for i in exchanges.keys():
        text = "\n".join((text, i, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text", ]) # Значеня для конвертации
def convert(message: telebot.types.Message):
    try:
       base, quote, amount = message.text.split() # Ошибки по количеству
    except ValueError as e:
        bot.reply_to(message, f"Не верное количество параметров!")

    try:
        new_price = Convertor.get_price(base, quote, amount)
        bot.reply_to(message, f"Цена {amount} {base} в {quote} : {new_price}")
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}" )



bot.polling(none_stop=True)