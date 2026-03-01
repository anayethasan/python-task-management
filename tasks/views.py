from urllib import request
from django.shortcuts import render, redirect
from django.http.request import HttpRequest 
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm, TaskDetailModelForm
from tasks.models import Employee, Project, Task, TaskDetail
from datetime import date
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from user.views import is_admin
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, DetailView, UpdateView

# Class based-view code
class Greeting(View):
    greet = "Hello niiloy i am every one"
    
    def get(self, request):
        return HttpResponse(self.greet)

class UpGreeting(Greeting):
    greet = "Noop your are write a wrong correct is hello every one i'm niloy"



# Create your views here.
def is_manager(user):
    return user.groups.filter(name='manager').exists()
def is_employee(user):
    return user.groups.filter(name='Employee').exists()

def is_manager_or_admin(user):
    return user.is_authenticated and (
        user.groups.filter(name='manager').exists() or
        user.is_superuser
    )

@user_passes_test(is_manager_or_admin, login_url='no-permission')
def manager_dashboard(request):
    #getting task count 
    # total_task = tasks.count()
    # completed_task = Task.objects.filter(status='COMPLETED').count()
    # in_progress_task = Task.objects.filter(status='IN_PROGRESS').count()
    # pending_task = Task.objects.filter(status='PENDING').count()
    
    type = request.GET.get('type', 'all')
    
    # tasks = Task.objects.select_related('details').prefetch_related('assigned_to').all()
    
    counts = Task.objects.aggregate(
        total = Count('id'),
        completed = Count('id', filter=Q(status='COMPLETED')),
        in_progress = Count('id', filter=Q(status='IN_PROGRESS')),
        pending = Count('id', filter=Q(status='PENDING')),
    )
    
    #Retriving task data
    
    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')
    
    if(type == 'completed'):
        tasks = base_query.filter(status='COMPLETED')
    elif(type == 'in-progress'):
        tasks = base_query.filter(status='IN_PROGRESS')
    elif(type == 'pending'):
        tasks = base_query.filter(status='PENDING')
    else:
        tasks = base_query.all()
    
    context = {
        "tasks": tasks,
        "counts": counts,
    }
    return render(request, "dashboard/dashboard.html", context)

def toppart(request):
    return render(request, "dashboard/toppart.html")

@user_passes_test(is_employee, login_url='no-permission')
def user_dashboard(request):
    return render(request, "dashboard/user_dashboard.html")

def test(request):
    return render(request, "test.html")

@login_required
@permission_required('tasks.add_task', login_url='no-permission')
def create_task(request):
    # employees = Employee.objects.all()
    # form = TaskForm(employees=employees)
    
    # if request.method == "POST":
    #     form = TaskForm(request.POST, employees=employees)
    #     if form.is_valid():
    #         data = form.cleaned_data
    #         title = data.get('title')
    #         description = data.get('description')
    #         due_date = data.get('due_date')
    #         assigned_to = data.get('assigned_to')
            
    #         task = Task.objects.create(title=title, description=description, due_date=due_date)
            
    #         #Assign task to employee
    #         for emp_id in assigned_to:
    #             employee = Employee.objects.get(id = emp_id)
    #             task.assigned_to.add(employee)
            
    #     return HttpResponse("Task Added Successfully")
    
    # context = {"form": form}
    # return render(request, "dashboard/task_form.html", context)


    # employees = Employee.objects.all()
    task_form = TaskModelForm()
    task_detail_form = TaskDetailModelForm()
    
    if request.method == "POST":
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
        
        if task_form.is_valid() and task_detail_form.is_valid():
            """For Model From data"""
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            
        messages.success(request, "Task Created Successfully done!")
        return redirect('create-task')
    
    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "dashboard/task_form.html", context)

create_decorators = [login_required, permission_required("tasks.add_task", login_url='no-permission')]
@method_decorator(create_decorators, name='dispatch')
class CreateTask(ContextMixin, LoginRequiredMixin, PermissionRequiredMixin, View):
    """ For creating task """
    permission_required = 'tasks.add_task'
    login_url = 'sign-in'
    template_name = 'dashboard/task_form.html'

    """ 
    0. Create Task
    1. LoginRequiredMixin
    2. PermissionRequiredMixin
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = kwargs.get('task_form', TaskModelForm())
        context['task_detail_form'] = kwargs.get(
            'task_detail_form', TaskDetailModelForm())
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)

        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Created Successfully")
            context = self.get_context_data(
                task_form=task_form, task_detail_form=task_detail_form)
            return render(request, self.template_name, context)

    

@login_required
@permission_required('tasks.change_task', login_url='no-permission')
def update_task(request, id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task) #get
    
    if task.details:
        task_detail_form = TaskDetailModelForm(instance=task.details)
    
    if request.method == "POST":
        task_form = TaskModelForm(request.POST, instance=task)
        task_detail_form = TaskDetailModelForm(request.POST, instance=task.details)
        
        if task_form.is_valid() and task_detail_form.is_valid():
            """For Model From data"""
            task = task_form.save()
            TaskDetail.objects.get_or_create(task=task)
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            
        messages.success(request, "Task update Successfully done!")
        return redirect('update_task', id)
    
    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "dashboard/task_form.html", context)

class UpdateTask(UpdateView):
    model = Task
    form_class = TaskModelForm
    template_name = 'task_form.html'
    context_object_name = 'task'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = self.get_form()
        print(context)
        if hasattr(self.object, 'details') and self.object.details:
            context['task_detail_form'] = TaskDetailModelForm(
                instance=self.object.details)
        else:
            context['task_detail_form'] = TaskDetailModelForm()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_form = TaskModelForm(request.POST, instance=self.object)

        task_detail_form = TaskDetailModelForm(
            request.POST, request.FILES, instance=getattr(self.object, 'details', None))

        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Updated Successfully")
            return redirect('update-task', self.object.id)
        return redirect('update-task', self.object.id)
    
@login_required
@permission_required('tasks.delete_task', login_url='no-permission')
def delete_task(request, id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=id)
            task.delete()
            messages.success(request, 'Task Deleted Successfully')
        except Task.DoesNotExist:
            messages.error(request, 'Task not found')
        return redirect('manager_dashboard')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('manager_dashboard')
    
    
def view_task(request):
    #retrive all data from task model
    # task = Task.objects.all()
    
    #retrive a specific task
    # task3 = Task.objects.get(id = 1)
    
    """Show the task that are completed"""
    # tasks = Task.objects.filter(status="COMPLETED")
    
    """show the data which date is today"""
    # tasks = Task.objects.filter(due_date=date.today())
    
    """Show the task whose priority is not low"""
    # tasks = TaskDetail.objects.exclude(Priority="L")
    
    """ Show the task that contain any word will have 'c' and status pending"""
    # tasks = Task.objects.filter(title__icontains="c", status="PENDING")
    
    """ Show the task which are pending or in_progress"""
    # tasks = Task.objects.filter(Q(status="PENDING") | Q(status="IN_PROGRESS"))
    
    """ Show the data when value exists"""
    # tasks = Task.objects.filter(status="PENDING").exists()
    
    """Selected_related(ForeignKey, OneToOne)"""
    # tasks = Task.objects.select_related('details').all()
    # tasks = TaskDetail.objects.select_related('task').all()
    # tasks = Task.objects.select_related('project').all()
    
    """ prefetch_related (reverse ForeignKey, manytomany) """
    tasks = Task.objects.prefetch_related("assigned_to").all()
    return render(request, "show_task.html", {"tasks" : tasks })

view_project_decorators = [login_required, permission_required(
    "projects.view_project", login_url='no-permission')]
@method_decorator(view_project_decorators, name='dispatch')
class ViewProject(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'show_task.html'

    def get_queryset(self):
        queryset = Project.objects.annotate(
            num_task=Count('task')).order_by('num_task')
        return queryset

@login_required
@permission_required("tasks.view_task", login_url='no-permission')
def task_details(request, task_id):
    task = Task.objects.get(id=task_id)
    status_choices = Task.STATUS_CHOICES

    if request.method == 'POST':
        selected_status = request.POST.get('task_status')
        print(selected_status)
        task.status = selected_status
        task.save()
        return redirect('task-details', task.id)

    return render(request, 'task_details.html', {"task": task, 'status_choices': status_choices})

class TaskDetail(DetailView):
    model = Task
    template_name = 'task_details.html'
    context_object_name = 'task'
    pk_url_kwarg = 'task_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # {"task": task}
        # {"task": task, 'status_choices': status_choices}
        context['status_choices'] = Task.STATUS_CHOICES
        return context

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        return redirect('task-details', task.id)

@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect('manager_dashboard')
    elif is_employee(request.user):
        return redirect('user_dashboard')
    elif is_admin(request.user):
        return redirect('admin-dashboard')

    return redirect('no-permission')

