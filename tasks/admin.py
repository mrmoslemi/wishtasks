from django.contrib import admin
from tasks.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ['creation', 'state', 'scheduled', 'callback', 'execution']


admin.site.register(Task, TaskAdmin)
