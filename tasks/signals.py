from django.db.models.signals import post_save, pre_save, post_delete, pre_delete, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from tasks.models import Task, TaskDetail, Project, Employee

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