# Generated by Django 3.2.9 on 2022-01-15 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='product_images/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pdf',
            field=models.FileField(upload_to='product_pdfs/'),
        ),
    ]
