# Generated by Django 3.2.7 on 2021-09-13 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontpage', '0002_alter_category_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]
