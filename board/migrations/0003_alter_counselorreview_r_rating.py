# Generated by Django 4.1 on 2023-08-24 05:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("board", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="counselorreview",
            name="r_rating",
            field=models.FloatField(default=0.0),
        ),
    ]
