# Generated by Django 4.1 on 2023-08-26 09:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("users", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("board", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="counselorreview",
            name="r_counselor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.counselor"
            ),
        ),
        migrations.AddField(
            model_name="counselorreview",
            name="r_patient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.patient"
            ),
        ),
        migrations.AddField(
            model_name="communication",
            name="com_patient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.patient"
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="article",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="board.article"
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="c_commenter",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="c_comment",
            name="cc_commenter",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="c_comment",
            name="communication",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="board.communication"
            ),
        ),
        migrations.AddField(
            model_name="article",
            name="a_patient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.patient"
            ),
        ),
    ]
