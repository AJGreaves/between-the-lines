# Generated by Django 5.1 on 2024-09-05 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_alter_book_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='summary',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
