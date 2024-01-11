from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.models import User


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The username field must be set')
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_moderator', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


# class Users(AbstractUser):
class Users(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True, serialize=False, verbose_name="ID")
    username = models.CharField(max_length=255, unique=True, verbose_name="Никнейм")
    password = models.CharField(max_length=255, verbose_name="Пароль")
    Is_Super = models.BooleanField(default=False, verbose_name="Является ли пользователь модератором?")

    # Necessary fields for django
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    # is_staff = models.BooleanField(default=False, verbose_name="Является ли пользователь менеджером?")
    # is_superuser = models.BooleanField(default=False, verbose_name="Является ли пользователь админом?")

    def str(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.username}"

    class Meta:
        db_table = 'Users'
        verbose_name = "Пользователь"


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

    Confirmation_Doctor = models.CharField(
        max_length=20,
        null=True,
        choices=[
            ('Pending', 'Ожидается'),
            ('Confirmed', 'Подтверждено'),
            ('Rejected', 'Отклонено'),
        ],
        default='Pending',
        help_text='Verbal confirmation of the Trauma'
    )

    def __str__(self):
        return f"{self.Trauma_ID}: {self.Creator}"

    @staticmethod
    def create_draft_trauma(creator_id):
        try:
            idTrauma = Trauma.objects.latest('Trauma_ID').Trauma_ID
        except Trauma.DoesNotExist:
            idTrauma = 0

        return Trauma.objects.create(
            Trauma_ID=idTrauma + 1,
            Status='Draft',
            Date_Creation=timezone.now(),
            Creator=Users.objects.filter(id=creator_id).first()
        )

    @staticmethod
    def get_draft_trauma(creator_id, create=False):
        if not Trauma.objects.filter(Status='Draft', Creator=Users.objects.filter(id=creator_id).first()).exists():
            if create:
                Trauma.create_draft_trauma(creator_id)
            else:
                return None
            # Trauma.create_draft_trauma(creator_id)
        return Trauma.objects.get(Status='Draft', Creator=Users.objects.filter(id=creator_id).first())


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
