# Generated by Django 4.1 on 2023-08-28 09:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("users", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("board", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="chat_room",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "r_article",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="board.article",
                    ),
                ),
                (
                    "r_counselor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.counselor",
                    ),
                ),
                (
                    "r_patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.patient"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="chat_message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("m_content", models.CharField(max_length=500)),
                (
                    "m_published_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date published"
                    ),
                ),
                (
                    "m_room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="chat.chat_room"
                    ),
                ),
                (
                    "m_writer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
