# Generated by Django 4.2.5 on 2023-12-06 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmstu_lab', '0003_categoriesprocedures_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoriesprocedures',
            name='ID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
