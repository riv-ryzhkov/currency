from django.db import models

from rate.utils import to_decimal

from rate import model_choices as mch


class Rate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    source = models.PositiveSmallIntegerField(choices=mch.SOURCE_CHOICES)
    currency = models.PositiveSmallIntegerField(choices=mch.CURRENCY_CHOICES)
    sale = models.DecimalField(max_digits=5, decimal_places=2)
    buy = models.DecimalField(max_digits=5, decimal_places=2)

    def save(self, *args, **kwargs):
        self.sale = to_decimal(self.sale)
        self.buy = to_decimal(self.buy)
        super().save(*args, **kwargs)