# Generated by Django 3.1.14 on 2023-12-14 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_article_view_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='view_count',
        ),
    ]
