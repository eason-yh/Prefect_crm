from django.contrib import admin
from crm import models
from django.shortcuts import render

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'qq', 'source', 'consultant', 'content', 'date')
    list_filter = ('source','consultant', 'date')
    search_fields = ('qq', 'name')
    raw_id_fields = ('consult_course',)
    filter_horizontal = ('tags',)
    #list_editable = ('status',)

    # actions = ["test_action",]
    #
    # def test_action(self,request,arg2,):
    #     print('test acction:',self,request,arg2)
    #     return render(request,"king_admin/table_obj_delete.html")

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','name')




admin.site.register(models.Customer,CustomerAdmin)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.Enrollment)
admin.site.register(models.Course)
admin.site.register(models.ClassList)
admin.site.register(models.CourseRecord)
admin.site.register(models.Branch)
admin.site.register(models.Role)
admin.site.register(models.Payment)
admin.site.register(models.StudyRecord)
admin.site.register(models.UserProfile)
admin.site.register(models.Menu)