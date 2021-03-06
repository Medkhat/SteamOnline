# Generated by Django 2.1.5 on 2019-09-03 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20190831_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='phone',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='video_lessons',
            name='image_video',
            field=models.ImageField(null=True, upload_to='image/lesson_video/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='iin',
            field=models.BigIntegerField(null=True),
        ),
    ]
