# -*- coding: utf-8 -

from django import forms


class CreditCardForm(forms.Form):
    stripe_token = forms.CharField(widget=forms.HiddenInput, required=False)
    card = forms.ChoiceField(widget=forms.Select(attrs={'style': 'width: 100%'}))

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', {})
        super(CreditCardForm, self).__init__(*args, **kwargs)
        for name, value in choices.iteritems():
            if value:
                self.fields[name].choices = value
