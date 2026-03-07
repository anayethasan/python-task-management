from django.contrib import admin
from tasks.models import Employee, Project, Task, TaskDetail
# from user.models import UserProfile

# Register your models here.
admin.site.register(Employee)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(TaskDetail)
# admin.site.register(UserProfile)