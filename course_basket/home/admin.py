from django.contrib import admin
from .models import Course
from import_export.admin import ImportExportModelAdmin

# Register your models here.
# admin.site.register(Course)

@admin.register(Course)
class ViewAdmin(ImportExportModelAdmin):
    pass
