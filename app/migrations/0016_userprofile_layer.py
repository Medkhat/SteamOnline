# Generated by Django 2.1.5 on 2019-11-21 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20191121_0733'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='layer',
            field=models.SmallIntegerField(default=0, null=True),
        ),
    ]
