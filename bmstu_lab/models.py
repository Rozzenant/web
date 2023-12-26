from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone


# from django.db.models.signals import post_migrate
# from django.db.models.signals import post_save
# from django.dispatch import receiver

class Users(models.Model):
    User_ID = models.IntegerField(primary_key=True)
    Is_Moderator = models.BooleanField(default=False)
    Username = models.CharField(max_length=48, help_text='Input your Username')
    Login = models.CharField(max_length=48, help_text='Input your Login')
    Password = models.CharField(max_length=48, help_text='Input your Password')

    def __str__(self):
        return self.Username


class First_aid(models.Model):
    First_aid_ID = models.IntegerField(primary_key=True)
    First_aid_Name = models.CharField(max_length=128, help_text='Input First aid Name')
    Description = models.TextField()
    Image_URL = models.ImageField(upload_to='img/', blank=True, editable=True)
    Price = models.FloatField(max_length=16)

    status = [
        ('0', 'Удален'),
        ('1', 'Действует'),
    ]

    Status = models.CharField(max_length=1, choices=status, default='1', help_text='Status First aid')

    def __str__(self):
        return self.First_aid_Name


class Trauma(models.Model):
    Trauma_ID = models.IntegerField(primary_key=True)
    # Trauma_Name = models.CharField(max_length=64, help_text='Input Trauma Name')

    status = [
        ('Draft', 'Черновик'),
        ('Formed', 'Сформирована'),
        ('Completed', 'Завершёна'),
        ('Cancelled', 'Отклонена'),
        ('Deleted', 'Удалёна'),
    ]

    Status = models.CharField(max_length=10, choices=status, default='Draft', help_text='Status Trauma')
    Date_Creation = models.DateTimeField(default=timezone.now, help_text='Date of Creating of the order (Trauma)')
    Date_Approving = models.DateTimeField(help_text='Date of Approving (Trauma)', null=True, blank=True)
    Date_End = models.DateTimeField(help_text='Date of End order (Trauma)', null=True, blank=True)
    Moderator = models.ForeignKey(Users, related_name='ID_Moderator', on_delete=models.CASCADE, null=True, blank=True)
    Creator = models.ForeignKey(Users, related_name='ID_Creator', on_delete=models.CASCADE)
    First_aid_in_Trauma_List = models.ManyToManyField(First_aid, through='First_aid_Trauma')

    def __str__(self):
        return f"{self.Trauma_ID}: {self.Creator}"

    @staticmethod
    def create_draft_trauma():
        try:
            idTrauma = Trauma.objects.latest('Trauma_ID').Trauma_ID
        except Trauma.DoesNotExist:
            idTrauma = 0

        return Trauma.objects.create(
            Trauma_ID=idTrauma + 1,
            Status='Draft',
            Date_Creation=timezone.now(),
            Creator=singleton()
        )

    @staticmethod
    def get_draft_trauma():
        if not Trauma.objects.filter(Status='Draft').exists():
            Trauma.create_draft_trauma()
        return Trauma.objects.get(Status='Draft')


class First_aid_Trauma(models.Model):
    First_aid_ID = models.ForeignKey(First_aid, on_delete=models.CASCADE)
    Trauma_ID = models.ForeignKey(Trauma, on_delete=models.CASCADE)

    class Meta:
        UniqueConstraint(fields=['Trauma_ID', 'First_aid_ID'], name='First_aid_in_Trauma_List')

    def __str__(self):
        return f"{self.Trauma_ID} - {self.First_aid_ID}"


def singleton():
    CREATOR_ID = Users.objects.get(User_ID=3)
    return CREATOR_ID
