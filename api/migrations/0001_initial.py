# Generated by Django 4.2.18 on 2025-03-02 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('developer', models.CharField(max_length=255)),
                ('year', models.PositiveIntegerField()),
                ('link', models.URLField()),
            ],
        ),
    ]
