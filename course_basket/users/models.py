from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from home.models import Course
from PIL import Image
# from django.contrib.postgres.fields import ArrayField

# Create your models here.

SEM_CHOICES = (
    ( 'sem1', '1st'),
    ( 'sem2', '2nd'),
    ('sem3', '3rd'),
    ('sem4', '4th'),
    ('sem5', '5th'),
    ('sem6', '6th'),
    ('sem7', '7th'),
    ('sem8', '8th')
)
BRANCH_CHOICES = (
    ('CSE', 'CSE'),
    ('DSE', 'DSE'),
    ('ME', 'ME'),
    ('EE', 'EE'),
    ('CE', 'CE'),
    ('BioE', 'BioE'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default = 'default.jpg', upload_to = 'profile_pics')
    rollno = models.CharField(default = "Not updated", max_length=30)
    sem = models.CharField(default = "1st", max_length=30, choices = SEM_CHOICES)
    branch = models.CharField(default="CSE",max_length=30, choices = BRANCH_CHOICES)
    completed_courses = models.ManyToManyField(Course, related_name='completed_courses', blank = True)
    current_courses = models.ManyToManyField(Course, related_name='current_courses', blank = True)
    # current_courses = models.ManyToManyField(Course, related_name='current_courses', blank = True)
    # current = ArrayField(Course, related_name='current_courses', blank = True)
    total_credits = models.IntegerField(default = 0)
    # liked_projects = models.ManyToManyField(Project, related_name='liked_projects', blank = True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
