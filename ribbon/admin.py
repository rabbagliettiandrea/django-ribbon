# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import

from django.contrib import admin
from django.utils.safestring import mark_safe

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.data import JsonLexer

from . import models


class _PrettyResponseMixin(object):
    def prettify_json(self, content):
        formatter = HtmlFormatter(style='colorful')
        prettified = highlight(content, JsonLexer(), formatter)
        return '<style>{}</style>{}'.format(formatter.get_style_defs(), prettified)

    def get_pretty_stripe_response(self, obj):
        return mark_safe('<br>{}'.format(self.prettify_json(obj.stripe_response)))


@admin.register(models.StripeCustomer)
class StripeCustomerAdmin(_PrettyResponseMixin, admin.ModelAdmin):
    list_display = ['__unicode__', 'user', 'timestamp_created']
    search_fields = ['stripe_id', 'user']
    readonly_fields = ['get_pretty_stripe_response']
    fields = ['stripe_id', 'user', 'get_pretty_stripe_response']


@admin.register(models.StripeCharge)
class StripeChargeAdmin(_PrettyResponseMixin, admin.ModelAdmin):
    list_display = ['__unicode__', 'stripe_customer', 'stripe_card', 'amount', 'currency', 'timestamp_created']
    readonly_fields = ['get_pretty_stripe_response']
    list_filter = ['currency']
    fields = ['stripe_id', 'stripe_customer', 'stripe_card', 'amount', 'currency', 'get_pretty_stripe_response']


@admin.register(models.StripeCard)
class StripeCardAdmin(_PrettyResponseMixin, admin.ModelAdmin):
    list_display = ['__unicode__', 'brand', 'country', 'funding', 'last4', 'exp_month', 'exp_year',
                    'timestamp_created']
    readonly_fields = ['get_pretty_stripe_response']
    list_filter = ['brand', 'country', 'funding']
    fields = ['stripe_id', 'stripe_customer', 'last4', 'exp_year', 'exp_month', 'brand', 'country',
              'funding', 'get_pretty_stripe_response']
