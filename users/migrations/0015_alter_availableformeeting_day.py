# Generated by Django 3.2.6 on 2021-12-31 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_instructor_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availableformeeting',
            name='day',
            field=models.CharField(blank=True, choices=[('Sunday', 'Sunday'), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')], max_length=255, null=True),
        ),
    ]