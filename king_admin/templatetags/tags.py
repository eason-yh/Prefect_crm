#!/usr/bin/env python
# -*- coding:utf-8 -*-


from django import template
from django.utils.safestring import mark_safe
import time

register = template.Library()

@register.simple_tag
def render_app_name(admin_class):
    return admin_class.model._meta.verbose_name

@register.simple_tag
def get_query_sets(admin_class):
    return admin_class.model.objects.all()

@register.simple_tag
def build_table_row(obj,admin_class):
    row_ele = ""

    for column in admin_class.list_display:
        field_obj = obj._meta.get_field(column)
        if field_obj.choices:
            column_data = getattr(obj,"get_%s_display" %column)()
        else:
            column_data = getattr(obj,column)
        if type(column_data).__name__ == 'datetime':

            column_data = column_data.strftime("%Y-%m-%d %H:%M:%S")

        row_ele += "<td>%s</td>" % column_data
    return mark_safe(row_ele)

@register.simple_tag
def build_paginators(query_sets,filter_condtions,previous_orderby, search_text):
    '''返回整个分页元素'''
    page_btns = ''
    filters = ''
    for k,v in filter_condtions.items():
        filters += "&%s=%s" %(k,v)
    added_dot_ele = False

    for page_num in query_sets.paginator.page_range:
        if page_num < 3 or page_num > query_sets.paginator.num_pages - 2 \
                or abs(query_sets.number - page_num) <= 2:#代表最前2页或最后2页
            ele_class = ""
            if query_sets.number == page_num:
                added_dot_ele == False
                ele_class = "active"
            page_btns += '''<li class="%s"><a href="?page=%s%s&o=%s&_q=%s">%s</a></li>''' % (
            ele_class, page_num, filters, previous_orderby,search_text, page_num)
        # elif abs(query_sets.number - page_num) <= 1:#判断前后1页
        #     ele_class = ""
        #     if query_sets.number == page_num:
        #         added_dot_ele == False
        #         ele_class = "active"
        #     page_btns += '''<li class="%s"><a href="?page=%s%s">%s</a></li>''' % (
        #     ele_class, page_num, filters, page_num)
        else:#显示...
            if added_dot_ele == False:
                page_btns += '<li><a>...</a></li>'
                added_dot_ele = True
    return mark_safe(page_btns)




@register.simple_tag
def render_page_ele(loop_counter,query_sets, filter_condtions):
    filters = ''
    for k,v in filter_condtions.items():
        filters += "&%s=%s" %(k,v)

    if loop_counter < 3 or loop_counter > query_sets.paginator.num_pages - 2:#代表这是前2页或后2页要显示
        ele_class = ""
        if query_sets.number == loop_counter:
            ele_class = "active"
        ele = '''<li class="%s"><a href="?page=%s%s">%s</a></li>''' %(ele_class,loop_counter,filters,loop_counter)
        return mark_safe(ele)
    if abs(query_sets.number - loop_counter) <= 2:
        ele_class = ""
        if query_sets.number == loop_counter:
            ele_class = "active"
        ele = '''<li class="%s"><a href="?page=%s%s">%s</a></li>''' %(ele_class,loop_counter,filters,loop_counter)
        return mark_safe(ele)
    else:
        return ''

@register.simple_tag
def render_filter_ele(condtion, admin_class, filter_condtions):
    select_ele = '''<select class="form-control", name='%s'><option value="">-----</option>''' %condtion
    filed_obj = admin_class.model._meta.get_field(condtion)
    if filed_obj.choices:
        selected = ''
        for choice_item in filed_obj.choices:
            if filter_condtions.get(condtion) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' %(choice_item[0],selected,choice_item[1])
            selected = ''
    if type(filed_obj).__name__ == "ForeignKey":
        selected = ''
        for choice_item in filed_obj.get_choices()[1:]:
            if filter_condtions.get(condtion) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0],selected,choice_item[1])
            selected = ''
    select_ele += "</select>"
    return mark_safe(select_ele)

@register.simple_tag
def build_table_header_column(column,orderby_key,filter_condtions):
    filters = ''
    for k,v in filter_condtions.items():
        filters += "&%s=%s" %(k,v)
    ele = '''<th><a href="?{filters}&o={orderby_key}">{column}</a>{sort_icon}</th>'''
    if orderby_key:
        if orderby_key.startswith("-"):
            sort_icon = '''<span class="glyphicon glyphicon-chevron-up" aria-hidden="true"></span>'''
        else:
            sort_icon = '''<span class="glyphicon glyphicon-chevron-down" aria-hidden="true"></span>'''
        if orderby_key.strip("-") == column:#排序当前字段
            orderby_key = orderby_key
        else:
            orderby_key = column
            sort_icon = ''
    else:#没有排序
        orderby_key = column
        sort_icon = ''
    ele = ele.format(orderby_key=orderby_key,column=column,sort_icon=sort_icon,filters=filters)
    return mark_safe(ele)


