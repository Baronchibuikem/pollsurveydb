# Generated by Django 3.0.6 on 2020-06-18 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20200618_0456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='poll_created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
