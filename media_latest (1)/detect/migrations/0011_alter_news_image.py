# Generated by Django 5.1.2 on 2025-02-09 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detect', '0010_news_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='news/'),
        ),
    ]
