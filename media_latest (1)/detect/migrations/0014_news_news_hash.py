# Generated by Django 5.1.2 on 2025-02-10 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0013_news_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='news_hash',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
