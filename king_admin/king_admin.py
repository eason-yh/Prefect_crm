#!/usr/bin/env python
# -*- coding:utf-8 -*-
from crm import models
from django.shortcuts import render,redirect

enabled_admin = { }

class BaseAdmin(object):
    list_display = []
    list_filters = []
    search_fields = []
    list_per_page = '3'
    ordering = None
    filter_horizontal = []
    actions = ["delete_selected_objs",]

    def delete_selected_objs(self,request,querysets):
        app_name = self.model._meta.app_label
        table_name = self.model._meta.model_name
        print("delete_selected_objs",self,request,querysets)
        if request.POST.get("delete_confirm") == "yes":
            querysets.delete()
            return redirect("/king_admin/%s/%s" % (app_name,table_name))
        selected_ids = ','.join([str(i.id) for i in querysets])
        return render(request,"king_admin/table_obj_delete.html",{"objs":querysets,
                                                                  "admin_class":self,
                                                                  "app_name":app_name,
                                                                  "table_name":table_name,
                                                                  "selected_ids":selected_ids,
                                                                  "action":request._admin_action,
        })


class CustomerAdmin(BaseAdmin):
    list_display = ['id', 'name', 'qq', 'source', 'consultant', 'consult_course', 'date']
    list_filters = ['source', 'consultant', 'consult_course', 'date', ]
    search_fields = ['qq', 'name', 'consultant__name', ]
    filter_horizontal = ('tags',)
    ordering = 'id'
    list_pre_page = 5

    actions = ["delete_selected_objs","test"]
    def test(self,request,querysets):
        print("in test")
    test.display_name = "测试"

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