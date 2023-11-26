# Generated by Django 4.2.7 on 2023-11-26 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramBotUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('step', models.IntegerField(choices=[(1, 'start')], default=1)),
            ],
        ),
    ]
