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
    r_content = models.CharField(max_length=200)
    r_rating = models.FloatField(default=0.0)

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


class C_Comment(models.Model):  # 소통게시판의 댓글모델
    cc_commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    cc_content = models.CharField(max_length=200)
    communication = models.ForeignKey(Communication, on_delete=models.CASCADE)

    def __str__(self):
        return self.cc_content


# 심리상담모델
class Mentalstate(models.Model):
    m_article = models.OneToOneField(Article, on_delete=models.CASCADE)
    aggression = models.IntegerField(null=True)  # 공격성
    anxiety = models.IntegerField(null=True)  # 불안감
    dependency = models.IntegerField(null=True)  # 의존성
    stress = models.IntegerField(null=True)  # 스트레스
    timidity = models.IntegerField(null=True)  # 소심함
    sociability = models.IntegerField(null=True)  # 사회성
    depression = models.IntegerField(null=True)  # 우울감
    independence = models.IntegerField(null=True)  # 독립성
    achievement = models.IntegerField(null=True)  # 성취감
    selfish = models.IntegerField(null=True)  # 이기적인

    def __str__(self):
        return self.m_article
