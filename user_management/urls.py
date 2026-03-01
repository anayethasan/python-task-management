from django.contrib import admin
from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path, include
from tasks.views import manager_dashboard, user_dashboard, toppart, test, create_task, view_task, update_task, delete_task, task_details, dashboard, Greeting, UpGreeting, CreateTask
from tasks.views import ViewProject, TaskDetail, UpdateTask
from core.views import home, no_permission
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("dashboard/", toppart),
    path("manager_dashboard/", manager_dashboard, name='manager_dashboard'),
    path("user_dashboard/", user_dashboard, name='user_dashboard'),
    path("test/", test),
    # path("create-task/", create_task, name='create-task'),
    path("create-task/", CreateTask.as_view(), name='create-task'),
    # path("view_task/", view_task, name='view-task'),
    path("view_task/", ViewProject.as_view(), name='view-task'),
    # path("task/<int:task_id>/details", task_details, name='task-details'),
    path("task/<int:task_id>/details", TaskDetail.as_view(), name='task-details'),
    # path("update_task/<int:id>/", update_task, name='update_task'),
    path("update_task/<int:id>/", UpdateTask.as_view(), name='update_task'),
    path("delete_task/<int:id>/", delete_task, name='delete_task'),
    path('user/', include("user.urls")),
    path('', home),
    path('no-permission/', no_permission, name='no-permission'),
    path('dashboard/', dashboard, name='dashboard'),
    path('greetings/', UpGreeting.as_view(), name='greetings'),
] + debug_toolbar_urls()


#for media file setup
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)