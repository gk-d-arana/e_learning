# Generated by Django 3.2.6 on 2022-01-01 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_tempwallet_money_before_edit'),
    ]

    operations = [
        migrations.AddField(
            model_name='tempwallet',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.branch'),
        ),
    ]