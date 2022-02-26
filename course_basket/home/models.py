from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# 'id': 'IC111',
# 'name': 'Linear Algebra',
# 'semester': '1',
# 'ltpc': '1-2-3-4',
# 'branch': 'ALL'

class Course(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    name = models.TextField()
    semester = models.CharField(max_length=5)
    ltpc = models.CharField(max_length=10)
    branch = models.CharField(max_length=10)
    current_user = models.ManyToManyField(User, related_name='AlreadyApplied', blank = True)

    def __str__(self):
        return self.name
