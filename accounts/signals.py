from django.db.models.signals import post_save, post_migrate, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Student, Instructor

# Create default groups after migrations
@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    Group.objects.get_or_create(name='Student')
    Group.objects.get_or_create(name='Instructor')
    print("Default groups created!")
 

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:  # Create profiles for new users
#         if instance.groups.filter(name='Students').exists():
#             Student.objects.get_or_create(user=instance)
#         elif instance.groups.filter(name='Instructors').exists():
#             Instructor.objects.get_or_create(user=instance)


# # Automatically create group profiles after group is created
# @receiver(post_save, sender=Group)
# def notify_group_creation(sender, instance, created, **kwargs):
#     if created:
#         print(f"Group {instance.name} created successfully.")








# python manage.py shell
'''
# Create groups
students_group, _ = Group.objects.get_or_create(name='Students')
instructors_group, _ = Group.objects.get_or_create(name='Instructors')

# Create users
user1 = User.objects.create_user(username='student1', password='password123')
user2 = User.objects.create_user(username='instructor1', password='password123')

# Add the user to the group (triggers the profile creation)
user1.groups.add(students_group)  # This will not automatically create a profile.
user2.groups.add(instructors_group)

# Save the user again to trigger post_save signal
user1.save()
user2.save()

# Now, check if profiles were created
print(user1.student_profile)  # Output: Student: student1
print(user2.instructor_profile)  # Output: Instructor: instructor1

//--------------
User.objects.create_user(username='asdf', password='password', groups=[Group.objects.get(name='Students')])

'''