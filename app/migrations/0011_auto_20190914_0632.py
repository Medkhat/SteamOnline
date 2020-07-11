# Generated by Django 2.1.5 on 2019-09-14 00:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20190903_1902'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sertificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.SmallIntegerField()),
                ('curs', models.CharField(max_length=200)),
                ('image', models.ImageField(default='image/sertificate/default.png', null=True, upload_to='image/sertificate/')),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='sertificate',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]