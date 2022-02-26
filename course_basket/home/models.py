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
    ltpc = models.CharField(default = "NONE",max_length=20)
    credits = models.IntegerField(default=0)
    # credits = models.IntField(default = 0)
    # semester = models.CharField(max_length=5)
    sem1 = models.CharField(default="NULL", max_length=5)
    sem2 = models.CharField(default="NULL", max_length=5)
    sem3 = models.CharField(default="NULL", max_length=5)
    sem4 = models.CharField(default="NULL", max_length=5)
    sem5 = models.CharField(default="NULL", max_length=5)
    sem6 = models.CharField(default="NULL", max_length=5)
    sem7 = models.CharField(default="NULL", max_length=5)
    sem8 = models.CharField(default="NULL", max_length=5)

    type = models.TextField(default="FE") #csv folder name

    # branch = models.CharField(max_length=10)
    # current_users = models.ManyToManyField(User, related_name='AlreadyApplied', blank = True)

    def __str__(self):
        return self.name


# import pandas as pd
# # from .models import Course

# xls = pd.ExcelFile('../Courses_Database.xlsx')

# sheet_names = xls.sheet_names

# courses = []
# for sheet in sheet_names:
#     dataset = pd.read_excel(xls, sheet)
#     for i in range(len(dataset)):
#         courses.append(Course(
#             id = dataset.iloc[i,0],
#             name = dataset.iloc[i,1],
#             ltpc = dataset.iloc[i,2],
#             sem1 = dataset.iloc[i,3],
#             sem2 = dataset.iloc[i,4],
#             sem3 = dataset.iloc[i,5],
#             sem4 = dataset.iloc[i,6],
#             sem5 = dataset.iloc[i,7],
#             sem6 = dataset.iloc[i,8],
#             sem7 = dataset.iloc[i,9],
#             sem8 =  dataset.iloc[i,10],
#             type = sheet
#             )
#         )

# Course.objects.bulk_create(courses)
