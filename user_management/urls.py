from django.contrib import admin
from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path, include
from tasks.views import manager_dashboard, user_dashboard, toppart, test, create_task, view_task, update_task, delete_task
from core.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path("dashboard/", toppart),
    path("manager_dashboard/", manager_dashboard, name='manager_dashboard'),
    path("user_dashboard/", user_dashboard),
    path("test/", test),
    path("create-task/", create_task, name='create-task'),
    path("view_task/", view_task),
    path("update_task/<int:id>/", update_task, name='update_task'),
    path("delete_task/<int:id>/", delete_task, name='delete_task'),
    path('user/', include("user.urls")),
    path('', home),
] + debug_toolbar_urls()
