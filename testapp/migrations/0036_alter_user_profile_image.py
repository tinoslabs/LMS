# Generated by Django 5.1.4 on 2025-01-16 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0035_alter_user_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, default='default/default_profile.jpg', upload_to='profile_images/'),
        ),
    ]
