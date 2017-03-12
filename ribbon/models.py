# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.formats import date_format


class _TimedatedModel(models.Model):
    timestamp_created = models.DateTimeField(auto_now_add=True, null=True, db_index=True, editable=False)
    timestamp_modified = models.DateTimeField(auto_now=True, null=True, db_index=True, editable=False)

    class Meta:
        abstract = True


class StripeCustomer(_TimedatedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    stripe_id = models.CharField(max_length=128, verbose_name='Stripe ID')
    stripe_response = JSONField()

    def __unicode__(self):
        return '{}'.format(self.stripe_id)


class StripeCard(_TimedatedModel):
    stripe_id = models.CharField(max_length=128, verbose_name='Stripe ID')
    stripe_customer = models.ForeignKey('StripeCustomer')
    stripe_response = JSONField()
    last4 = models.CharField(max_length=4)
    exp_year = models.PositiveSmallIntegerField()
    exp_month = models.PositiveSmallIntegerField()
    brand = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    funding = models.CharField(max_length=64)

    def __unicode__(self):
        return '**** **** **** {} ({}) - Exp: {}/{}'.format(self.last4, self.brand, self.exp_year, self.exp_month)


class StripeCharge(_TimedatedModel):
    stripe_id = models.CharField(max_length=128, verbose_name='Stripe ID')
    stripe_customer = models.ForeignKey('StripeCustomer')
    stripe_card = models.ForeignKey('StripeCard')
    stripe_response = JSONField()
    amount = models.PositiveIntegerField()
    currency = models.CharField(max_length=10)

    def get_amount_display(self):
        amount_unicode = unicode(self.amount)
        return '{}.{}'.format(amount_unicode[:-2], amount_unicode[-2:])

    def __unicode__(self):
        return '[{}] [{}] {} {}'.format(
            date_format(self.timestamp_created, settings.DATETIME_FORMAT),
            self.stripe_card,
            self.get_amount_display(),
            self.currency
        )
