import requests
from celery import shared_task

from rate.utils import to_decimal
from rate import model_choices as mch


@shared_task
def parse_privatbank():
    from rate.models import Rate

    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(url)
    print(response.json())

    currency_mapper = {
        'USD': mch.CURRENCY_USD,
        'EUR': mch.CURRENCY_EUR,
    }

    for r in response.json():

        if r['ccy'] not in currency_mapper:
            continue

        sale = to_decimal(r['sale'])
        buy = to_decimal(r['buy'])
        currency = currency_mapper[r['ccy']]

        latest_rate = Rate.objects.filter(
            source=mch.SOURCE_PRIVATBANK,
            currency=currency,
        ).last()  # Rate() or None

        if latest_rate is None or latest_rate.sale != sale or latest_rate.buy != buy:
            Rate.objects.create(
                source=mch.SOURCE_PRIVATBANK,
                currency=currency,
                buy=buy,
                sale=sale,
            )


@shared_task
def parse_monobank():
    print('parse_monobank')

@shared_task
def parse():
    parse_privatbank.delay()
    parse_monobank.delay()