from urllib import request
from django.shortcuts import render, redirect
from django.http.request import HttpRequest 
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm, TaskDetailModelForm
from tasks.models import Employee, Project, Task, TaskDetail
from datetime import date
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib import messages

# Create your views here.
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

def user_dashboard(request):
    return render(request, "dashboard/user_dashboard.html")

def test(request):
    return render(request, "test.html")

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
        task_detail_form = TaskDetailModelForm(request.POST)
        
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
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            
        messages.success(request, "Task update Successfully done!")
        return redirect('update_task', id)
    
    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "dashboard/task_form.html", context)
    
def delete_task(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, "Task Deleted successfully done !")
        return redirect('manager_dashboard')
    else:
        messages.error(request, 'Can not get the operation something wrong')
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

