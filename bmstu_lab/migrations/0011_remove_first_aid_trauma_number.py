# Generated by Django 4.2.5 on 2023-12-18 01:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bmstu_lab', '0010_alter_trauma_date_approving_alter_trauma_date_end_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='first_aid_trauma',
            name='Number',
        ),
    ]
