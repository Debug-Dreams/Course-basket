# Generated by Django 4.0.2 on 2022-02-26 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_course_sem1_alter_course_sem2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='ltpc',
            field=models.CharField(default='NONE', max_length=20),
        ),
    ]
