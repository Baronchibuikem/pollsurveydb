# Generated by Django 3.0.6 on 2020-06-18 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20200606_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='choice_name',
            field=models.CharField(max_length=250),
        ),
    ]