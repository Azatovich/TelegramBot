import requests
import json
from config import exchanges

class APIException(Exception):
    pass

class Convertor: # Функционал для обработки ошибок
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = exchanges[base.title()]
        except KeyError:
            return APIException(f"Валюта {base} не найдена!")

        try:
            quote_key = exchanges[quote.title()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        if base_key == quote_key:
            raise APIException(f"Не возможно перевести одинаковые валюты {base}!")

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}!")

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={base_key}&from={quote_key}&amount={amount}" # Сервер для получения данных по курсу валют
        API_KEY = 'uDtKJfbmuWgvYOxHYPcAZQynJEz92P5e'
        payload = {}
        headers = {
            "apikey": API_KEY
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        resp = json.loads(response.content)

        new_price = resp['result']
        return round(new_price, 3)