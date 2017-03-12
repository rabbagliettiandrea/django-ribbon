# -*- coding: utf-8 -

from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.views import generic

import ribbon.handlers
from ribbon.example import forms


class RibbonView(generic.FormView):
    template_name = 'ribbon_example/pay.html'
    form_class = forms.PayForm

    def get_success_url(self):
        return self.request.path

    def get_form_kwargs(self):
        kwargs = super(RibbonView, self).get_form_kwargs()
        choices = kwargs.setdefault('choices', {})

        choices['card'] = []
        if hasattr(self.request.user, 'stripecustomer'):
            for stripe_card in self.request.user.stripecustomer.stripecard_set.all():
                choices['card'].append((stripe_card.pk, stripe_card))
        choices['card'].append(('-1', '-- Add new card --'))

        return kwargs

    def form_valid(self, form):
        user = self.request.user
        stripe_token = form.cleaned_data['stripe_token']
        charge = float(form.cleaned_data['charge'])
        stripe_card_pk = form.cleaned_data['card']
        if stripe_card_pk != '-1':
            stripe_card = self.request.user.stripecustomer.stripecard_set.get(pk=stripe_card_pk)
        elif stripe_token:
            if hasattr(self.request.user, 'stripecustomer'):
                stripe_card = ribbon.handlers.old_customer__new_card(customer=user.stripecustomer, token=stripe_token)
            else:
                stripe_card = ribbon.handlers.new_customer__new_card(user=user, token=stripe_token)
        else:
            return HttpResponseBadRequest('Bad request: no card/stripe_token in POST request')

        amount = '{:.2f}'.format(charge).replace('.', '')
        stripe_charge = ribbon.handlers.charge(card=stripe_card, amount=amount)
        messages.success(self.request, 'Payment done!')
        return super(RibbonView, self).form_valid(form)
