import json
import requests
from config import API_KEY
from config import list_of_currencies

class APIException(Exception):
    pass

# Для Ковертации курсов использую API сайта www.currencyconverterapi.com
# quote - валюта 1
# base - валюта, в которую переводим
# amount - кол-во валюты 1

class Convertor:
    @staticmethod
    def get_price(values):
        if len(values) != 3:
            raise APIException("Неверное количество параметров")
        quote, base, amount = values
        if quote == base:
            raise APIException(f"Вы ввели одинаковые валюты: {base}")
        try:
            quote_formated = list_of_currencies[quote]
        except KeyError:
            raise APIException(f"Такая валюта не поддерживается: {quote}")
        try:
            base_formated = list_of_currencies[base]
        except KeyError:
            raise APIException(f"Такая валюта не поддерживается: {base}")
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не корректно введено количество валюты: {amount}")

        query = str(quote_formated + "_" + base_formated)
        html = requests.get(f'https://free.currconv.com/api/v7/convert?q={query}&compact=ultra&apiKey={API_KEY}')
        # print(html.content)
        result = (json.loads(html.content)[query]) * amount
        # print(result)
        return round(result, 2)

