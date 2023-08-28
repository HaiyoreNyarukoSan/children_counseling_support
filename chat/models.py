from django.db import models
from board.models import Article
from users.models import Patient, Counselor, User


class chat_room(models.Model):
    r_counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE, null=True)
    r_patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    r_article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'c:{self.r_counselor.c_user.username} p:{self.r_patient.p_name}, a:{self.r_article.a_title}'


class chat_message(models.Model):
    m_writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    m_room = models.ForeignKey(chat_room, on_delete=models.CASCADE, null=True),
    m_content = models.CharField(max_length=500, null=True)
    m_published_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return f'{self.m_writer.username} {self.m_content[:10]}'
