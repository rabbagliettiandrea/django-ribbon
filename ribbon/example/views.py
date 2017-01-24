# -*- coding: utf-8 -
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.views import generic

from ribbon import mixins
from ribbon.example import forms


class RibbonView(mixins.StripeMixin, generic.FormView):
    template_name = 'ribbon_example/pay.html'
    form_class = forms.PayForm

    def get_form_kwargs(self):
        kwargs = super(RibbonView, self).get_form_kwargs()
        if hasattr(self.request.user, 'stripecustomer'):
            kwargs['cards'] = self.request.user.stripecustomer.stripecard_set.all()
        return kwargs

    def post(self, request, *args, **kwargs):
        charge = int(request.POST['charge'])
        if request.POST.get('card', '-1') != '-1':
            stripe_card = self.request.user.stripecustomer.stripecard_set.get(pk=request.POST['card'])
        elif 'stripeToken' in request.POST:
            token = request.POST['stripeToken']
            if hasattr(request.user, 'stripecustomer'):
                stripe_card = self.old_customer__new_card(customer=request.user.stripecustomer, token=token)
            else:
                stripe_card = self.new_customer__new_card(user=request.user, token=token)
        else:
            return HttpResponseBadRequest('Bad request: no card/stripeToken in POST request')

        amount = '{:.2f}'.format(charge).replace('.', '')
        self.charge(card=stripe_card, amount=amount)

        messages.success(request, 'Payment done!')
        return redirect(request.path)

