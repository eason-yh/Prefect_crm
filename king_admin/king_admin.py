#!/usr/bin/env python
# -*- coding:utf-8 -*-
from crm import models
from django.shortcuts import render,redirect
from django.utils.translation import ugettext as _


enabled_admin = { }

class BaseAdmin(object):
    list_display = []
    list_filters = []
    search_fields = []
    list_per_page = '3'
    ordering = None
    filter_horizontal = []
    readonly_fields = []
    readonly_table = False
    actions = ["delete_selected_objs",]
    modelform_exclude_fields = []

    def delete_selected_objs(self,request,querysets):
        app_name = self.model._meta.app_label
        table_name = self.model._meta.model_name
        print("delete_selected_objs",self,request,querysets)
        if self.readonly_table:
            errors = {"readonly_table":"this table is readonly,cannot be deleted or modified"}
        else:
            errors = {}

        if request.POST.get("delete_confirm") == "yes":
            if not self.readonly_table:
                querysets.delete()
            return redirect("/king_admin/%s/%s" % (app_name,table_name))
        selected_ids = ','.join([str(i.id) for i in querysets])
        return render(request,"king_admin/table_obj_delete.html",{"objs":querysets,
                                                                  "admin_class":self,
                                                                  "app_name":app_name,
                                                                  "table_name":table_name,
                                                                  "selected_ids":selected_ids,
                                                                  "action":request._admin_action,
                                                                  "errors":errors,})

    def default_form_validation(self):
        '''用户可以在此进行自定义的表单验证，相当于django form的clean方法'''

        pass

class UserProfileAdmin(BaseAdmin):
    list_display = ('email', 'name',)
    readonly_fields = ('password',)
    modelform_exclude_fields = ["last_login"]
    filter_horizontal = ('user_permissions','groups')

class CustomerAdmin(BaseAdmin):
    list_display = ['id', 'name', 'qq', 'source', 'consultant', 'consult_course', 'date', 'enroll']
    list_filters = ['source', 'consultant', 'consult_course', 'date', ]
    search_fields = ['qq', 'name', 'consultant__name', ]
    filter_horizontal = ('tags',)
    ordering = 'id'
    list_pre_page = 5
    readonly_fields = ["qq", "consultant", "tags"]
    readonly_table = True
    #modelform_exclude_fields = []

    actions = ["delete_selected_objs","test"]
    def test(self,request,querysets):
        print("in test")
    test.display_name = "测试"

    def enroll(self):
        return '''<a href="%s/enrollment/">报名</a>''' %self.instance.id
    enroll.display_name = "报名链接         "

    def default_form_validation(self):
        # print("------customer validation", self)
        # print("------instance",self.instance)

        consult_content = self.cleaned_data.get("content")
        if len(consult_content) < 15:
            return self.ValidationError(
                                    _('Field %(field)s 咨询内容记录不能少于15个字符'),
                                    code='invalid',
                                    params={'field': "content",},
                                )

    def clean_name(self):
        print("name clean validation",self.cleaned_data["name"])
        if not self.cleaned_data ["name"]:
            self.add_error('name',"can't be null ")




class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ('customer', 'consultant', 'date')


def register(models_class,admin_class=None):
    if models_class._meta.app_label not in enabled_admin:
        enabled_admin[models_class._meta.app_label] = { }

    #admin_obj = admin_class()
    admin_class.model = models_class
    enabled_admin[models_class._meta.app_label][models_class._meta.model_name] = admin_class


register(models.UserProfile,UserProfileAdmin)
register(models.Customer,CustomerAdmin)
register(models.CustomerFollowUp,CustomerFollowUpAdmin)