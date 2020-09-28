# Generated by Django 3.0.7 on 2020-09-23 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=60, null=True)),
                ('lastname', models.CharField(max_length=60, null=True)),
                ('ip_address', models.CharField(blank=True, max_length=30)),
                ('email', models.EmailField(max_length=100, null=True)),
                ('message', models.TextField(max_length=500, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
