# Generated by Django 5.0.3 on 2024-04-14 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Connections',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User', models.CharField(max_length=60)),
                ('Book', models.CharField(max_length=30)),
            ],
        ),
    ]
