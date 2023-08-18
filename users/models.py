from django.contrib.auth.models import AbstractUser
from django.db import models

GENDER_CHOICES = [
    ('M', '남성'),
    ('F', '여성'),
]


# Create your models here.
class User(AbstractUser):
    u_birthday = models.DateField("생년월일")
    u_gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    u_contact = models.IntegerField()


class Patient(models.Model):
    p_user = models.ForeignKey(User, on_delete=models.CASCADE)
    p_gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    p_birthday = models.DateField("생년월일")


class Counselor(models.Model):
    c_user = models.ForeignKey(User, on_delete=models.CASCADE)
    c_certificate = models.ImageField("썸네일 이미지", upload_to='article', blank=True, null=True)  # 자격증
    c_department = models.TextField()  # 전문 분야
    c_resume = models.TextField()  # 이력서
