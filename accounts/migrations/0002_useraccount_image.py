# Generated by Django 5.0.2 on 2024-06-14 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='accounts/media/uploads/'),
        ),
    ]
