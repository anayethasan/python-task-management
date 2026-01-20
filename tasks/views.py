from django.shortcuts import render
from django.http.request import HttpRequest 
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Project, Task, TaskDetail
from datetime import date
from django.db.models import Q

# Create your views here.
def manager_dashboard(request):
    return render(request, "dashboard/dashboard.html")

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


    employees = Employee.objects.all()
    form = TaskModelForm()
    
    if request.method == "POST":
        form = TaskModelForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'dashboard/task_form.html', {"form": form, "message": "Task Added Successfully"})
    
    context = {"form": form}
    return render(request, "dashboard/task_form.html", context)


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