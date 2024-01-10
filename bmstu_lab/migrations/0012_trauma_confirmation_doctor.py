# Generated by Django 4.2.5 on 2024-01-10 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmstu_lab', '0011_remove_first_aid_trauma_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='trauma',
            name='confirmation_doctor',
            field=models.CharField(choices=[('Pending', 'Ожидается'), ('Confirmed', 'Подтверждено'), ('Rejected', 'Отклонено')], default='Pending', help_text='Verbal confirmation of the Trauma', max_length=20),
        ),
    ]
