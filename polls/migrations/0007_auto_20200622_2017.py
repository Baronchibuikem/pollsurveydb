# Generated by Django 3.0.6 on 2020-06-22 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20200621_1409'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='poll',
            options={'ordering': ('-id',)},
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set(),
        ),
    ]