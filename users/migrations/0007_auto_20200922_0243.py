# Generated by Django 3.0.7 on 2020-09-22 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20200921_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='ip_address',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='email',
            field=models.EmailField(max_length=100, null=True),
        ),
    ]
