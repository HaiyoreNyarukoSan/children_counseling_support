# Generated by Django 4.1 on 2023-08-25 07:37

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Article",
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
                ("a_title", models.CharField(max_length=200)),
                ("a_content", models.CharField(max_length=200)),
                (
                    "a_published_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date published"
                    ),
                ),
                (
                    "a_tree_image",
                    models.ImageField(
                        blank=True, upload_to="htp/tree", verbose_name="나무 이미지"
                    ),
                ),
                (
                    "a_man_image",
                    models.ImageField(
                        blank=True, upload_to="htp/man", verbose_name="남자사람 이미지"
                    ),
                ),
                (
                    "a_woman_image",
                    models.ImageField(
                        blank=True, upload_to="htp/woman", verbose_name="여자사람 이미지"
                    ),
                ),
                (
                    "a_house_image",
                    models.ImageField(
                        blank=True, upload_to="htp/house", verbose_name="집 이미지"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="C_Comment",
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
                ("cc_content", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
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
                ("c_content", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Communication",
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
                ("com_title", models.CharField(max_length=200)),
                ("com_content", models.CharField(max_length=200)),
                (
                    "com_published_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date published"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CounselorReview",
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
                ("r_content", models.CharField(max_length=200)),
                ("r_rating", models.FloatField(default=0.0)),
            ],
        ),
    ]
