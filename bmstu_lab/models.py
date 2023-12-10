from django.db import models


class Users(models.Model):
    User_ID = models.IntegerField(primary_key=True)
    Is_Admin = models.BooleanField(default=False)
    Username = models.CharField(max_length=48, help_text='Input your Username')
    Login = models.CharField(max_length=48, help_text='Input your Login')
    Password = models.CharField(max_length=48, help_text='Input your Password')

    def __str__(self):
        return self.Username


class MedicalProcedures(models.Model):
    Procedure_ID = models.IntegerField(primary_key=True)
    Procedure_Name = models.CharField(max_length=128, help_text='Input Procedure Name')
    Description = models.TextField()
    # Image_URL = models.CharField(max_length=128)
    Image_URL = models.ImageField(upload_to='img/', blank=True, editable=True)
    Price = models.FloatField(max_length=16)

    status = [
        ('0', 'Удален'),
        ('1', 'Действует'),
    ]

    Status = models.CharField(max_length=1, choices=status, default='1', help_text='Status Procedure')

    def __str__(self):
        return self.Procedure_Name


class MedicalCategories(models.Model):
    MedicalCategories_ID = models.IntegerField(primary_key=True)
    Category_Name = models.CharField(max_length=64, help_text='Input Category Name')
    Description = models.TextField()
    Image_URL = models.ImageField(upload_to='img/', blank=True, editable=True)

    status = [
        ('i', 'Введён'),
        ('w', 'В работе'),
        ('e', 'Завершён'),
        ('c', 'Отменён'),
        ('d', 'Удалён'),
    ]

    Status = models.CharField(max_length=1, choices=status, default='i', help_text='Status Category')
    Date_Creation = models.DateField(default='01.01.1900', help_text='Date of receipt of the order')
    Date_Approving = models.DateField(default='01.01.1900', help_text='Date of Approving order')
    Date_End = models.DateField(default='01.01.1900', help_text='Date of End order')
    Moderator = models.ForeignKey(Users, on_delete=models.CASCADE)
    ID_Creator = models.ForeignKey(Users, related_name='ID_Author', on_delete=models.CASCADE, default=1)
    MedicalProceduresList = models.ManyToManyField(MedicalProcedures, through='CategoriesProcedures')

    def __str__(self):
        return self.Category_Name


class CategoriesProcedures(models.Model):
    ID = models.AutoField(primary_key=True)
    Procedure_ID = models.ForeignKey(MedicalProcedures, on_delete=models.CASCADE)
    Category_ID = models.ForeignKey(MedicalCategories, on_delete=models.CASCADE)
    Number = models.IntegerField(null=True, help_text='Порядковый номер', default=1)

    def __str__(self):
        return f"{self.Procedure_ID} - {self.Category_ID}"
