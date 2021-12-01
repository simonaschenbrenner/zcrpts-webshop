# Generated by Django 3.2.9 on 2021-12-01 00:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=100)),
                ('text', models.TextField(max_length=500)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_flagged', models.BooleanField(default=False)),
                ('helpful', models.PositiveIntegerField(default=0)),
                ('not_helpful', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ['product', 'timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField()),
                ('picture', models.ImageField(blank=True, null=True, upload_to='product_pictures/')),
            ],
            options={
                'verbose_name': 'Product Picture',
                'verbose_name_plural': 'Product Pictures',
                'ordering': ['product', 'order'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('version', models.CharField(max_length=20)),
                ('short_description', models.CharField(max_length=200)),
                ('long_description', models.CharField(blank=True, max_length=1000)),
                ('file', models.FileField(upload_to='product_files/')),
                ('pdf', models.FileField(blank=True, null=True, upload_to='product_pdfs/')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ['title', 'version'],
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5)])),
            ],
            options={
                'verbose_name': 'Product Rating',
                'verbose_name_plural': 'Product Ratings',
                'ordering': ['product', 'myuser'],
            },
        ),
    ]
