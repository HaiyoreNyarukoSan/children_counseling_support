# Generated by Django 4.1 on 2023-08-29 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0002_remove_chat_message_m_room_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="chat_message",
            name="m_room",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="chat.chat_room",
            ),
        ),
    ]
