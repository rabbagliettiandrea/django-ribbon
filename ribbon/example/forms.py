# -*- coding: utf-8 -

from django import forms

from ribbon.forms import CreditCardListForm


class PayForm(CreditCardListForm):
    CHARGE_CHOICES = [
        ('10', '10 usd'),
        ('20', '20 usd'),
        ('50', '50 usd'),
        ('100', '100 usd')
    ]
    card = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width: 100%'}))
    charge = forms.ChoiceField(choices=CHARGE_CHOICES, widget=forms.RadioSelect(), initial='10')

    def __init__(self, cards=None, *args, **kwargs):
        super(PayForm, self).__init__(*args, **kwargs)
        self.fields['card'].choices = []
        if cards:
            self.fields['card'].choices.extend([(card.id, card) for card in cards])
        self.fields['card'].choices.append(('-1', '-- Add new card --'))
