# Generated by Django 5.0.4 on 2025-02-04 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyDiplom', '0005_images_lord'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='image_prc',
            field=models.ImageField(default=None, upload_to=''),
        ),
        migrations.AlterField(
            model_name='images',
            name='image',
            field=models.ImageField(default=None, upload_to=''),
        ),
    ]
