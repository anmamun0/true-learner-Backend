from django.db.models.signals import post_save, post_migrate, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Student, Instructor

# Create default groups after migrations
@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    Group.objects.get_or_create(name='Students')
    Group.objects.get_or_create(name='Instructors')
    print("Default groups created!")
 

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:  # Create profiles for new users
        if instance.groups.filter(name='Students').exists():
            Student.objects.get_or_create(user=instance)
        elif instance.groups.filter(name='Instructors').exists():
            Instructor.objects.get_or_create(user=instance)


# # Automatically create group profiles after group is created
# @receiver(post_save, sender=Group)
# def notify_group_creation(sender, instance, created, **kwargs):
#     if created:
#         print(f"Group {instance.name} created successfully.")
