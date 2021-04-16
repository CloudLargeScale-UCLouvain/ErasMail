# Generated by Django 3.1.6 on 2021-04-22 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0038_auto_20210422_0059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailstats',
            name='newsletters_unsubscribed_count',
        ),
        migrations.AddField(
            model_name='emailstats',
            name='newsletters_erasmail_unsubscribed_count',
            field=models.PositiveIntegerField(default=0, help_text='Number of newsletters that have been unsubscribed using ErasMail'),
        ),
    ]
