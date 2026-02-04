"""
URL configuration for user_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path, include
from tasks.views import manager_dashboard, user_dashboard, toppart, test, create_task, view_task, update_task, delete_task
from core.views import home

urlpatterns = [
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
