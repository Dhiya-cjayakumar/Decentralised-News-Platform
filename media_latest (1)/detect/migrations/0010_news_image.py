# Generated by Django 5.1.2 on 2025-02-09 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0009_news_us_behave'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='image',
            field=models.ImageField(default=1, upload_to='news/'),
            preserve_default=False,
        ),
    ]
