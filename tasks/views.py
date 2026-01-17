from django.shortcuts import render
from django.http.request import HttpRequest 
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Project, Task, TaskDetail

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