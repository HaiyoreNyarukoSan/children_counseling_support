from django.db import models

from users.models import Patient, Counselor, User


# Create your models here.
class Article(models.Model):
    a_patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    a_title = models.CharField(max_length=200)
    a_content = models.CharField(max_length=200)
    # 글 작성일
    a_published_date = models.DateTimeField('date published', auto_now_add=True)
    # 상담용 그림들
    a_tree_image = models.ImageField("나무 이미지", upload_to='htp/tree', blank=True)
    a_man_image = models.ImageField("남자사람 이미지", upload_to='htp/man', blank=True)
    a_woman_image = models.ImageField("여자사람 이미지", upload_to='htp/woman', blank=True)
    a_house_image = models.ImageField("집 이미지", upload_to='htp/house', blank=True)

    def __str__(self):
        return self.a_title


class Comment(models.Model):
    c_commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    c_content = models.CharField(max_length=200)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.c_content


class CounselorReview(models.Model):
    r_patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    r_counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE)
    r_rating = models.FloatField()

    def __str__(self):
        return f'{self.r_patient} rated {self.r_counselor} {self.r_rating}'


class Communication(models.Model):
    com_patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    com_title = models.CharField(max_length=200)
    com_content = models.CharField(max_length=200)
    # 글 작성일
    com_published_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return self.com_title
