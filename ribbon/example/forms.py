# -*- coding: utf-8 -

from django import forms

from ribbon.forms import CreditCardForm


class PayForm(CreditCardForm):
    CHARGE_CHOICES = [
        ('10', '10 usd'),
        ('20', '20 usd'),
        ('50', '50 usd'),
        ('100', '100 usd')
    ]
    charge = forms.ChoiceField(choices=CHARGE_CHOICES, widget=forms.RadioSelect(), initial='10')
