from celery import shared_task

from rate import model_choices as mch
from rate.utils import to_decimal

import requests


@shared_task
def parse_privatbank():
    from rate.models import Rate
    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(url)
    # print(response.json())
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
        print('!!!PRIVAT!!!!', latest_rate.source, latest_rate.currency, latest_rate.sale, latest_rate.buy)


@shared_task
def parse_monobank():
    from monobank_api import BaseAPI
    from rate.models import Rate
    mono = BaseAPI()
    response = mono.get_currency()
    # print('response!!!!!!!!!!!!!!!!!!!', response[0])
    currency_mapper = {
        '840': mch.CURRENCY_USD,
        '978': mch.CURRENCY_EUR,
    }
    for r in response:
        # print(r['currencyCodeA'])
        if (str(r['currencyCodeA']) not in currency_mapper) or str(r['currencyCodeB']) != '980':
            # print(r['currencyCodeA'] * 10)
            continue
        sale = to_decimal(r['rateSell'])
        buy = to_decimal(r['rateBuy'])
        currency = currency_mapper[str(r['currencyCodeA'])]
        latest_rate = Rate.objects.filter(
            source=mch.SOURCE_MONOBANK,
            currency=currency,
        ).last()  # Rate() or None
        print('!!!MONOBANK!!!!', latest_rate.source, latest_rate.currency, latest_rate.sale, latest_rate.buy)
        if latest_rate is None or latest_rate.sale != sale or latest_rate.buy != buy:
            Rate.objects.create(
                source=mch.SOURCE_MONOBANK,
                currency=currency,
                buy=buy,
                sale=sale,
            )


@shared_task
def parse_vkurse():
    from rate.models import Rate
    url = 'http://vkurse.dp.ua/course.json'
    response = requests.get(url)
    # print(response.json())
    currency_mapper = {
        'Dollar': mch.CURRENCY_USD,
        'Euro': mch.CURRENCY_EUR,
    }
    for r in response.json():
        if r not in currency_mapper:
            # print('r[xxxxxxx]', r)
            continue
        sale = to_decimal(response.json()[r]['sale'])
        buy = to_decimal(response.json()[r]['buy'])
        currency = currency_mapper[r]
        latest_rate = Rate.objects.filter(
            source=mch.SOURCE_VKURSE,
            currency=currency,
        ).last()  # Rate() or None
        print('!!VKURSE!!!!', latest_rate.source, latest_rate.currency, latest_rate.sale, latest_rate.buy)
        # Rate.objects.create(
        #     source=mch.SOURCE_VKURSE,
        #     currency=currency,
        #     buy=buy,
        #     sale=sale,
        # )
        if latest_rate is None or latest_rate.sale != sale or latest_rate.buy != buy:
            Rate.objects.create(
                source=mch.SOURCE_VKURSE,
                currency=currency,
                buy=buy,
                sale=sale,
            )
# http://vkurse.dp.ua/course.json


@shared_task
def parse_dnipro():
    from rate.models import Rate
    url = 'https://kurstoday.com/api/average/Dnipro'
    response = requests.get(url)
    # print(response.json())
    currency_mapper = {
        'usd': mch.CURRENCY_USD,
        'eur': mch.CURRENCY_EUR,
    }
    for r in response.json():
        if r not in currency_mapper:
            # print('r[DNIPRO!!!!!!!!!!!]', r)
            continue
        sale = to_decimal(response.json()[r]['sel'])
        buy = to_decimal(response.json()[r]['buy'])
        currency = currency_mapper[r]
        latest_rate = Rate.objects.filter(
            source=mch.SOURCE_DNIPRO,
            currency=currency,
        ).last()  # Rate() or None
        # print('!!!!!!!!!!!!!!', latest_rate.source, latest_rate.currency, latest_rate.sale, latest_rate.buy)
        # Rate.objects.create(
        #     source=mch.SOURCE_DNIPRO,
        #     currency=currency,
        #     buy=buy,
        #     sale=sale,
        # )
        print('!!DNIPRO!!!!!!!!!!!!', latest_rate.source, latest_rate.currency, latest_rate.sale, latest_rate.buy)
        if latest_rate is None or latest_rate.sale != sale or latest_rate.buy != buy:
            Rate.objects.create(
                source=mch.SOURCE_DNIPRO,
                currency=currency,
                buy=buy,
                sale=sale,
            )


@shared_task
def parse_nbu():
    from rate.models import Rate
    url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'
    response = requests.get(url)
    # print(response.json())
    currency_mapper = {
        'USD': mch.CURRENCY_USD,
        'EUR': mch.CURRENCY_EUR,
    }
    for r in response.json():
        if r['cc'] not in currency_mapper:
            continue
        sale = to_decimal(r['rate'])
        buy = to_decimal(r['rate'])
        currency = currency_mapper[r['cc']]
        latest_rate = Rate.objects.filter(
            source=mch.SOURCE_NBU,
            currency=currency,
        ).last()  # Rate() or None
        # Rate.objects.create(
        #     source=mch.SOURCE_NBU,
        #     currency=currency,
        #     buy=buy,
        #     sale=sale,
        # )
        if latest_rate is None or latest_rate.sale != sale or latest_rate.buy != buy:
            Rate.objects.create(
                source=mch.SOURCE_NBU,
                currency=currency,
                buy=buy,
                sale=sale,
            )
        print('!!!NBU!!!!', latest_rate.source, latest_rate.currency, latest_rate.sale, latest_rate.buy)


@shared_task
def parse():
    parse_privatbank.delay()
    parse_monobank.delay()
    parse_vkurse.delay()
    parse_dnipro.delay()
    parse_nbu.delay()
# [
#   {
#     "currencyCodeA": 840,
#     "currencyCodeB": 980,
#     "date": 1552392228,
#     "rateSell": 27,
#     "rateBuy": 27.2,
#     "rateCross": 27.1
#   }
# ]
