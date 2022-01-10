# Generated by Django 3.2.9 on 2021-12-24 01:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/'),
        ),
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together={('product', 'myuser')},
        ),
    ]