# -*- coding: utf-8 -

from __future__ import unicode_literals, division, absolute_import

import json

import stripe
from django.conf import settings

from . import models


def _json_dump_response(response):
    return json.dumps(dict(response), skipkeys=True, indent=4)


class StripeMixin(object):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    def new_customer__new_card(self, user, token):
        response_customer = stripe.Customer.create(
            source=token, description="serverable User ID: {}".format(user.pk), email=user.email
        )
        stripe_customer = models.StripeCustomer.objects.create(
            user=user,
            stripe_id=response_customer.stripe_id,
            stripe_response=_json_dump_response(response_customer)
        )
        response_card = response_customer.sources.data[0]
        stripe_card = models.StripeCard.objects.create(
            stripe_id=response_card.id,
            stripe_customer=stripe_customer,
            stripe_response=_json_dump_response(response_card),
            last4=response_card.last4,
            exp_year=response_card.exp_year,
            exp_month=response_card.exp_month,
            brand=response_card.brand,
            country=response_card.country,
            funding=response_card.funding
        )
        return stripe_card

    def old_customer__new_card(self, customer, token):
        response_customer = stripe.Customer.retrieve(customer.stripe_id)
        response_card = response_customer.sources.create(source=token)
        stripe_card = models.StripeCard.objects.create(
            stripe_id=response_card.id,
            stripe_customer=customer,
            stripe_response=_json_dump_response(response_card),
            last4=response_card.last4,
            exp_year=response_card.exp_year,
            exp_month=response_card.exp_month,
            brand=response_card.brand,
            country=response_card.country,
            funding=response_card.funding
        )
        return stripe_card

    def charge(self, card, amount):
        response_charge = stripe.Charge.create(
            amount=amount, currency="usd", source=card.stripe_id, customer=card.stripe_customer
        )
        stripe_charge = models.StripeCharge.objects.create(
            stripe_id=response_charge.stripe_id,
            stripe_customer=card.stripe_customer,
            stripe_card=card,
            stripe_response=_json_dump_response(response_charge),
            amount=response_charge.amount,
            currency=response_charge.currency,
        )
        return stripe_charge
