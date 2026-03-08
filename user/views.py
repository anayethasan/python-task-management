from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group
# from django.contrib.auth.models import User 
from django.contrib.auth import login, logout, authenticate
from user.forms import CustomRegistrationForm, LoginForm, AssignRoleForm, CreateGroupForm, ChangePasswordForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm
from django.contrib import messages
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.views.generic import TemplateView, UpdateView, CreateView, ListView
from django.urls import reverse_lazy
from user.forms import EditProfileForm
from django.contrib.auth import get_user_model
from django.views import View


#Test for user
User = get_user_model()

"""
class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['userprofile'] = UserProfile.objects.get(user=self.request.user)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = UserProfile.objects.get(user=self.request.user)
        print("views", user_profile)
        context['form'] = self.form_class(
            instance=self.object, userprofile=user_profile)
        return context

    def form_valid(self, form):
        form.save(commit=True)
        return redirect('profile')
"""
class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        form.save(commit=True)
        return redirect('profile')
    
    

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def sign_up(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False
            user.save()
            
            messages.success(
                request, 'A Confirmation mail sent. Please check your email')
            return redirect('sign-in')
        else:
            print("Form is not valid")
    return render(request, 'registration.html', {"form": form})
# sign_up class based view
class SignUp(CreateView):
    form_class = CustomRegistrationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('sign-in')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password1'))
        user.is_active = False
        user.save()
        messages.success(
                self.request, 'A Confirmation mail sent. Please check your email')
        return redirect(self.success_url)
    
    def form_invalid(self, form):
        print('Form is not valid')
        return super().form_invalid(form)
    
    

def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'login.html', {'form': form})

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()

class ChangePassword(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    form_class = ChangePasswordForm

@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')
    
# ActivateUser class based view
class ActivateUser(View):

    def get(self, request, user_id, token):
        try:
            user = User.objects.get(id=user_id)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return redirect('sign-in')
            else:
                return HttpResponse('Invalid Id or token')

        except User.DoesNotExist:
            return HttpResponse('User not found')   
    
# admin dashboard using class based view
@method_decorator(user_passes_test(is_admin, login_url='no-permission'), name='dispatch')
class AdminDashboard(ListView):
    model = User
    template_name = 'admin/dashboard.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        return User.objects.prefetch_related(
            Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
        ).all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        for user in context['users']:
            if user.all_groups:
                user.groups_name = user.all_groups[0].name
            else:
                user.groups_name = 'No Groups Assigned'

        return context

# assign role class based view
@method_decorator(user_passes_test(is_admin, login_url='no-permission'), name='dispatch')
class AssignRole(View):
    template_name = 'admin/assign_role.html'
    
    def get_user(self, user_id):
        return User.objects.get(id=user_id)
    
    def get(self, request, user_id):
        user = self.get_user(user_id)
        form = AssignRoleForm()
        return render(request, self.template_name, {'form': form, 'user': user})
    
    def post(self, request, user_id):
        user = self.get_user(user_id)
        form = AssignRoleForm(request.POST)
        
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear() #Remove old roles
            user.groups.add(role)
            messages.success(request, f"User {user.username} has been assign to the {role.name} role")
            return redirect('admin-dashboard')
        return render(request, self.template_name, {'form': form, 'user': user})


# class based create view
@method_decorator(user_passes_test(is_admin, login_url='no-permission'), name='dispatch')
class CreateGroup(CreateView):
    model = Group
    form_class = CreateGroupForm
    template_name = 'admin/create_group.html'
    success_url = reverse_lazy('group-list')
    
    def form_valid(self, form):
        group = form.save();
        messages.success(self.request, f'Group {group.name} has been created successfully')
        return redirect(self.success_url)
    
    
# group list view
@method_decorator(user_passes_test(is_admin, login_url='no-permission'), name='dispatch')
class GroupList(ListView):
    model = Group
    template_name = 'admin/group_list.html'
    context_object_name = 'groups'
    
    def get_queryset(self):
        return Group.objects.prefetch_related('permissions').all()

class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user = self.request.user
        
        context['name'] = user.get_full_name()
        context['email'] = user.email
        context['username'] = user.username
        context['bio'] = user.bio
        context['profile_image'] = user.profile_image
        
        
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        
        return context
    
class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')
    html_email_template_name = 'registration/reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        print(context)
        return context

    def form_valid(self, form):
        messages.success(
            self.request, 'A Reset email sent. Please check your email')
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign-in')

    def form_valid(self, form):
        messages.success(
            self.request, 'Password reset successfully')
        return super().form_valid(form)