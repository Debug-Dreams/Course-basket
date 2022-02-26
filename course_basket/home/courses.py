import pandas as pd
from .models import Course

xls = pd.ExcelFile('../Courses_Database.xlsx')

sheet_names = xls.sheet_names

courses = []
for sheet in sheet_names:
    dataset = pd.read_excel(xls, sheet)
    for i in range(len(dataset)):
        courses.append(Course(
            id = dataset.iloc[i,0],
            name = dataset.iloc[i,1],
            ltpc = dataset.iloc[i,2],
            sem1 = dataset.iloc[i,3],
            sem2 = dataset.iloc[i,4],
            sem3 = dataset.iloc[i,5],
            sem4 = dataset.iloc[i,6],
            sem5 = dataset.iloc[i,7],
            sem6 = dataset.iloc[i,8],
            sem7 = dataset.iloc[i,9],
            sem8 =  dataset.iloc[i,10],
            type = sheet
            )
        )

Course.objects.bulk_create(courses)


