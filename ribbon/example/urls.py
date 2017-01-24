# -*- coding: utf-8 -

from django.conf.urls import url


from . import views


urlpatterns = [
    url(r'^$', views.RibbonView.as_view(), name='ribbon_view'),
]
