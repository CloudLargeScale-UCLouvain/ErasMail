# Generated by Django 3.1.6 on 2021-02-19 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0005_auto_20210217_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='sender_email',
            field=models.EmailField(default='e@a.c', max_length=254),
            preserve_default=False,
        ),
    ]
