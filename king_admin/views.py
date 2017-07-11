from django.shortcuts import render,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from king_admin import king_admin
from king_admin.utils import table_filter, table_sort, table_search
from king_admin.forms import create_model_form
import importlib



def index(request):
    return render(request, "king_admin/table_index.html",{'table_list':king_admin.enabled_admin})


def display_table_objs(request, app_name, table_name):
    print("-->",app_name,table_name)
    #model_module = importlib.import_module('%s.models'%(app_name))
    #model_obj = getattr(model_module,table_name)
    admin_class = king_admin.enabled_admin[app_name][table_name]
    #object_list = admin_class.model.objects.all()
    if request.method == "POST":#action 来了

        print(request.POST)
        selected_ids = request.POST.get("selected_ids")
        action = request.POST.get("action")
        if selected_ids:
            selected_objs = admin_class.model.objects.filter(id__in=selected_ids.split(','))
        else:
            raise KeyError("No object selected")
        if hasattr(admin_class,action):
            action_func = getattr(admin_class,action)
            request._admin_action = action
            return action_func(admin_class,request,selected_objs)


    object_list, filter_condtions = table_filter(request,admin_class)#过滤后的结果
    object_list = table_search(request,admin_class,object_list)
    object_list,orderby_key = table_sort(request,admin_class,object_list)#排序后的结果
    paginator = Paginator(object_list, admin_class.list_per_page) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        query_sets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        query_sets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        query_sets = paginator.page(paginator.num_pages)


    return render(request,"king_admin/table_objs.html",{"admin_class":admin_class,
                                                              "query_sets":query_sets,
                                                        "filter_condtions":filter_condtions,
                                                        "orderby_key":orderby_key,
                                                        "previous_orderby": request.GET.get("o", '') ,
                                                        "search_text": request.GET.get('_q',''),})

def table_obj_delete(request,app_name,table_name,obj_id):
    admin_class = king_admin.enabled_admin[app_name][table_name]
    objs = admin_class.model.objects.filter(id=obj_id)

    if request.method == "POST":
        objs.delete()
        return redirect("/king_admin/%s/%s" %(app_name,table_name))

    return render(request,"king_admin/table_obj_delete.html",{"app_name": app_name,
                                                              "table_name": table_name,
                                                              "admin_class":admin_class,
                                                              "objs": objs,})

def table_obj_add(request,app_name,table_name):
    admin_class = king_admin.enabled_admin[app_name][table_name]
    model_form_class = create_model_form(request,admin_class)
    if request.method == "POST":
        form_obj = model_form_class(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(request.path.replace("/add/",""))
    else:
            form_obj = model_form_class()

    return render(request, "king_admin/table_obj_add.html", {"form_obj":form_obj,
                                                             'admin_class': admin_class,
                                                             'app_name':app_name,})


def table_obj_change(request,app_name,table_name,obj_id):

    admin_class = king_admin.enabled_admin[app_name][table_name]
    model_form_class = create_model_form(request,admin_class)
    obj = admin_class.model.objects.get(id=obj_id)
    if request.method == "POST":
        form_obj = model_form_class(request.POST,instance=obj)#更新
        if form_obj.is_valid():
            form_obj.save()
    else:
        #obj = admin_class.model.objects.get(id=obj_id)
        form_obj = model_form_class(instance=obj)

    return render(request, "king_admin/table_obj_change.html",{"form_obj":form_obj,
                                                               'admin_class':admin_class,
                                                               "app_name": app_name,
                                                               "table_name": table_name,})