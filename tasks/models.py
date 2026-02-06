from django.db import models
from django.db.models.signals import post_save, pre_save, post_delete, pre_delete, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail

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
#post_save 
# @receiver(post_save, sender=Task)
# def notify_task_creation(sender, instance, created, **kwargs):
#     print('sender', sender)
#     print('instance', instance)
#     print(kwargs)
#     print(created)
#     if created:
#         instance.is_completed = True
#         instance.save()
        
#for pre_save
# @receiver(pre_save, sender=Task)
# def notify_task_creation_pre(sender, instance, created, **kwargs):
#     print('sender', sender)
#     print('instance', instance)
#     print(kwargs)
    
#     instance.is_completed = True

#for post_delete
# @receiver(post_delete, sender=Task)
# def notify_task_deletion_post(sender, instance, **kwargs):
#     print("====== POST DELETE SIGNAL ======")
#     print("sender:", sender)
#     print("instance:", instance)
#     print("instance.id:", instance.id)
#     print("instance.title:", instance.title)
#     print("instance.is_completed:", instance.is_completed)
#     print("kwargs:", kwargs)
        
# @receiver(pre_delete, sender=Task)
# def notify_task_deletion_pre(sender, instance, **kwargs):
#     print("====== PRE DELETE SIGNAL ======")
#     print("sender:", sender)
#     print("instance:", instance)
#     print("instance.id:", instance.id)
#     print("instance.title:", instance.title)
#     print("instance.is_completed:", instance.is_completed)
#     print("kwargs:", kwargs)

@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_employee_on_task_creation(sender, instance, action, **kwargs):
    print(instance, instance.assigned_to.all())
    
    assigned_emails = [emp.email for emp in instance.assigned_to.all()]
    print('Checking......', assigned_emails)
    
    send_mail(
        "New Task Assigned",
        f"You have been assigned to the this task : --> {instance.title}",
        "slashupdates@gmail.com",
        assigned_emails,
        fail_silently=False,
    )
    
    
@receiver(post_delete, sender=Task)
def delete_associate_details(sender, instance, **kwargs):
    if instance.details:
        print(isinstance)
        instance.details.delete()
        
        print('Delete successfully!')