from django.urls import path
# from user.views import activate_user
from core.views import home
from user.views import CustomLoginView, ProfileView, ChangePassword, CustomPasswordResetView, CustomPasswordResetConfirmView, EditProfileView
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from user.views import CreateGroup, GroupList, AssignRole, AdminDashboard, SignUp, ActivateUser

urlpatterns = [
    # path('sign-up/', sign_up, name='sign-up'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    # path('sign-in/', sign_in, name='sign-in'),
    path('sign-in/', CustomLoginView.as_view(), name='sign-in'),
    # path('sign-out/', sign_out, name='logout'),
    path('sign-out/', LogoutView.as_view(), name='logout'),
    path('home/', home, name='home'),
    path('activate/<int:user_id>/<str:token>/', ActivateUser.as_view(), name='activate'),
    # path('admin-dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin-dashboard/', AdminDashboard.as_view(), name='admin-dashboard'),
    # path('admin/<int:user_id>/assign-role/', assign_role, name='assign-role'),
    path('admin/<int:user_id>/assign-role/', AssignRole.as_view(), name='assign-role'),
    # path('admin/create-group/', create_group, name='create-group'),
    path('admin/create-group/', CreateGroup.as_view(), name='create-group'),
    # path('admin/group-list/', group_list, name='group-list'),
    path('admin/group-list/', GroupList.as_view(), name='group-list'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit-profile/', EditProfileView.as_view(), name='edit-profile'),
    path('password-change/', ChangePassword.as_view(), name='change-password'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name = 'accounts/password_change_done.html'), name='password-change-done'),
     path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/',
         CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm')
]
