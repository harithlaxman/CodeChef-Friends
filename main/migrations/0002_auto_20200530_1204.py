# Generated by Django 3.0.6 on 2020-05-30 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='frienddetails',
            name='user',
        ),
        migrations.AddField(
            model_name='user',
            name='friend',
            field=models.ManyToManyField(blank=True, to='main.FriendDetails'),
        ),
    ]
