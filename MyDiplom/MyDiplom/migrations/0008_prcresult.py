# Generated by Django 5.0.4 on 2025-02-06 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyDiplom', '0007_remove_images_image_prc_images_prc_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prcresult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prc_image_name', models.CharField(default=None, max_length=30)),
                ('prc_status', models.CharField(default=None, max_length=30)),
            ],
        ),
    ]
