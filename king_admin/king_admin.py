#!/usr/bin/env python
# -*- coding:utf-8 -*-
from crm import models

enabled_admin = { }

class BaseAdmin(object):
    list_display = []
    list_filters = []
    search_fields = []
    list_per_page = '3'
    ordering = None
    filter_horizontal = []

class CustomerAdmin(BaseAdmin):
    list_display = ['id', 'name', 'qq', 'source', 'consultant', 'consult_course', 'date']
    list_filters = ['source', 'consultant', 'consult_course', 'date', ]
    search_fields = ['qq', 'name', 'consultant__name', ]
    filter_horizontal = ('tags',)
    ordering = 'id'

class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ('customer', 'consultant', 'date')


def register(models_class,admin_class=None):
    if models_class._meta.app_label not in enabled_admin:
        enabled_admin[models_class._meta.app_label] = { }

    #admin_obj = admin_class()
    admin_class.model = models_class
    enabled_admin[models_class._meta.app_label][models_class._meta.model_name] = admin_class



register(models.Customer,CustomerAdmin)
register(models.CustomerFollowUp,CustomerFollowUpAdmin  )