#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.forms import forms, ModelForm

from crm import models

class CustomerModelForm(ModelForm):
    class Meta:
        model = models.Customer
        fields = "__all__"

def create_model_form(request,admin_class):
    '''动态生成ModelForm'''
    class Meta:
        model = admin_class.model
        fields = "__all__"

    attrs = {'Meta':Meta}
    _model_form_class = type("DynamicModelForm",(ModelForm,),attrs)
    #setattr(_model_form_class,'Meta',Meta)
    return _model_form_class