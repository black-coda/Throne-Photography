# Generated by Django 3.2.7 on 2022-06-16 23:17

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20220616_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='descriptive_photo',
            field=models.ImageField(blank=True, max_length=150, null=True, upload_to=main.models.category_dir_file),
        ),
    ]
