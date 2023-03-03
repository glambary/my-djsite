import requests
from bs4 import BeautifulSoup
# from decimal import Decimal as D, ROUND_HALF_UP

URL = "https://mironline.ru/support/list/kursy_mir/?sphrase_id=99648"
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36'
}


def get_exchange_rate_bel_rub():
    error = 'Функция "get_exchange_rate_bel_rub" отработала некорректно'
    rate = 0.001

    try:
        response = requests.get(URL, headers=headers)
    except Exception as err:
        print(error + " - ошибка в опредления response", err)

    if not response:
        print(error, ' - response')
        return rate
    soup = BeautifulSoup(response.text, "lxml")
    data = soup.select("tr td p")
    for indx, value in enumerate(data):
        if 'Белорусский рубль' in value.text:
            rate = data[indx + 1].text.strip().replace(',', '.')
            break
    else:
        print(error, ' - for')
        return rate
    return round(float(rate), 2)


def main():
    print(get_exchange_rate_bel_rub())


if __name__ == '__main__':
    main()
