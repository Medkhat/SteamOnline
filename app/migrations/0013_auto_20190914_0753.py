# Generated by Django 2.1.5 on 2019-09-14 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_userprofile_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='points',
            field=models.SmallIntegerField(default=0, null=True),
        ),
    ]