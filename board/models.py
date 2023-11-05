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


DATA_CATEGORY = ['나무', '남자사람', '여자사람', '집']
LABELS = {
    '나무': ['나무전체', '기둥', '수관', '가지', '뿌리', '나뭇잎', '꽃', '열매', '그네', '새', '다람쥐', '구름', '달', '별'],
    '남자사람': ['사람전체', '머리', '얼굴', '눈', '코', '입', '귀', '머리카락', '목', '상체', '팔', '손', '다리', '발', '단추', '주머니', '운동화',
             '남자구두'],
    '여자사람': ['사람전체', '머리', '얼굴', '눈', '코', '입', '귀', '머리카락', '목', '상체', '팔', '손', '다리', '발', '단추', '주머니', '운동화',
             '여자구두'],
    '집': ['집전체', '지붕', '집벽', '문', '창문', '굴뚝', '연기', '울타리', '길', '연못', '산', '나무', '꽃', '잔디', '태양']
}

agreeableness = '우호성'
conscientiousness = '성실성'
extraversion = '외향성'
neuroticism = '신경성'
openness_to_experience = '경험에 대한 개방성'

STAT_TYPE = (agreeableness, conscientiousness, extraversion, neuroticism, openness_to_experience)


# 심리상담모델
class Mentalstate(models.Model):
    m_article = models.OneToOneField(Article, on_delete=models.CASCADE)
    # aggression = models.IntegerField(null=True)  # 공격성
    # anxiety = models.IntegerField(null=True)  # 불안감
    # dependency = models.IntegerField(null=True)  # 의존성
    # stress = models.IntegerField(null=True)  # 스트레스
    # timidity = models.IntegerField(null=True)  # 소심함
    # sociability = models.IntegerField(null=True)  # 사회성
    # depression = models.IntegerField(null=True)  # 우울감
    # independence = models.IntegerField(null=True)  # 독립성
    # achievement = models.IntegerField(null=True)  # 성취감
    # selfish = models.IntegerField(null=True)  # 이기적인
    agreeableness = models.IntegerField(null=True)  # 우호성
    conscientiousness = models.IntegerField(null=True)  # 성실성
    extraversion = models.IntegerField(null=True)  # 외향성
    neuroticism = models.IntegerField(null=True)  # 신경성
    openness_to_experience = models.IntegerField(null=True)  # 경험에 대한 개방성

    STAT_TYPE = (agreeableness, conscientiousness, extraversion, neuroticism, openness_to_experience)

    def __str__(self):
        value = "\n".join(
            f'{field.name}: {field.value}' for field in self._meta.fields if field.get_internal_type == 'IntegerField')
        return value
