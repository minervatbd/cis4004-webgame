# Generated by Django 4.2.18 on 2025-03-18 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='title',
            field=models.CharField(default='defaultTitle', max_length=255),
        ),
    ]
