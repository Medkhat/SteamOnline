# Generated by Django 2.1.5 on 2019-09-15 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20190914_0753'),
    ]

    operations = [
        migrations.AddField(
            model_name='curs',
            name='type_curs',
            field=models.SmallIntegerField(default=5, null=True),
        ),
    ]
