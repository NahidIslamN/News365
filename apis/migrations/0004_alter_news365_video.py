# Generated by Django 5.2 on 2025-05-01 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0003_alter_news365_created_at_alter_news365_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news365',
            name='video',
            field=models.TextField(blank=True, null=True),
        ),
    ]
