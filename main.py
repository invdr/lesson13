from datetime import datetime
import requests
import json
import os

API_KEY = os.getenv('EXCHANGE_API_KEY')
CURRENCY_RATES_FILE = 'currency.json'

def main():
    while True:
        currency = input("Enter currency (USD or EUR): ")
        if currency not in ('USD', 'EUR'):
            print("Incorrect input")
            continue

        rate = get_currency_rate(currency)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print(f'{currency} course to RUBLE {rate}: ')
        data = {'currency': currency, 'rate': rate, 'timestamp': timestamp}
        save_to_json(data)

        user_choice = input("Choice (1 - continue, 2 - exit): ")
        if user_choice == '1':
            continue
        elif user_choice == '2':
            break
        else:
            print("Incorrect input")


def get_currency_rate(base: str):
    """Get course from API and return float."""
    url = "https://api.apilayer.com/exchangerates_data/latest"
    response = requests.get(url, headers={'apikey': API_KEY}, params={'base': base})
    rate = response.json()['rates']['RUB']
    return rate


def save_to_json(data: dict) -> None:
    """Save data to json file"""
    with open(CURRENCY_RATES_FILE, 'a', encoding='utf8') as f:
        if os.stat(CURRENCY_RATES_FILE).st_size == 0:
            json.dump([data], f)
        else:
            with open(CURRENCY_RATES_FILE, encoding='utf8') as f:
                data_list = json.load(f)
                data_list.append(data)
            with open(CURRENCY_RATES_FILE, 'w', encoding='utf8') as f:
                json.dump(data_list, f)





if __name__ == '__main__':
    main()