# Generated by Django 3.2.6 on 2022-01-07 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0018_auto_20220107_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='myeditorialquestion',
            name='answer_as_image',
            field=models.FileField(blank=True, null=True, upload_to='static/images'),
        ),
    ]