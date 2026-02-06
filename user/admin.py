from django.contrib import admin
from tasks.models import Employee, Project, Task, TaskDetail

# Register your models here.
admin.site.register(Employee)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(TaskDetail)