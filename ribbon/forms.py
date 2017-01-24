# -*- coding: utf-8 -

from django import forms


class CreditCardListForm(forms.Form):
    card = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width: 100%'}))

    def __init__(self, cards=None, *args, **kwargs):
        super(CreditCardListForm, self).__init__(*args, **kwargs)
        self.fields['card'].choices = []
        if cards:
            self.fields['card'].choices.extend([(card.id, card) for card in cards])
        self.fields['card'].choices.append(('-1', '-- Add new card --'))
