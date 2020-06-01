from monobank_api import BaseAPI

mono = BaseAPI()
currencies = mono.get_currency()

print(currencies)
for r in currencies:
    print(r['currencyCodeA'])
