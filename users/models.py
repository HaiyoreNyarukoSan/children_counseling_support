from django.contrib.auth.models import AbstractUser
from django.db import models

GENDER_CHOICES = [
    ('M', '남성'),
    ('F', '여성'),
]

PATIENT_GROUP = 'patient'
COUNSELOR_GROUP = 'counselor'


# Create your models here.
class User(AbstractUser):
    u_nickname = models.CharField(max_length=15, null=True)
    u_birthday = models.DateField("생년월일", null=True)
    u_gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    u_contact = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.username} - {self.get_full_name()}'


class Patient(models.Model):
    p_user = models.ForeignKey(User, on_delete=models.CASCADE)
    p_name = models.CharField(max_length=100)
    p_gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    p_birthday = models.DateField("생년월일", null=True)

    def __str__(self):
        return f'{self.p_user.username} - {self.p_name}'


class Counselor(models.Model):
    c_user = models.ForeignKey(User, on_delete=models.CASCADE)
    c_certificate = models.ImageField("썸네일 이미지", upload_to='article', blank=True, null=True)  # 자격증
    c_department = models.TextField(null=True)  # 전문 분야
    c_resume = models.TextField(null=True)  # 이력서

    def __str__(self):
        return f'{self.c_user.username} - counselor'
