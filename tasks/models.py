from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    
    def __str__(self):
        return self.name
    
class Employee(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    #task_set
    
    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed")
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)
    assigned_to = models.ManyToManyField(Employee, related_name='tasks')
    title = models.CharField(max_length=250)
    description = models.TextField()
    status = models.CharField(max_length=250, choices=STATUS_CHOICES, default="PENDING")
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    #taskdetail_set ei name eikhane column toiri hoye gese
    
    def __str__(self):
        return self.title


#one to one 
#Many to Many
#Many to One

class TaskDetail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_OPTIONS = (
        (HIGH, 'HIGH'),
        (MEDIUM, 'MEDIUM'),
        (LOW, 'LOW')
    )
    
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='details')
    
    # assigned_to = models.CharField(max_length=100)
    Priority = models.CharField(max_length=2, choices=PRIORITY_OPTIONS, default=MEDIUM)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Details Form Task {self.task.title}"
    
    
#Many to One
