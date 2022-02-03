# Generated by Django 3.2.9 on 2022-01-11 02:56

import Products.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField(max_length=500)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_flagged', models.BooleanField(default=False)),
                ('rate', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ['product', 'timestamp'],
            },
        ),
        migrations.CreateModel(
            name='LicenseKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('licenseKey', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pictures', models.FileField(upload_to=Products.models.get_image_filename)),
            ],
            options={
                'verbose_name': 'Product Picture',
                'verbose_name_plural': 'Product Pictures',
                'ordering': ['product'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('version', models.CharField(max_length=100)),
                ('price', models.FloatField(default=0)),
                ('short_description', models.CharField(max_length=200)),
                ('long_description', models.TextField(blank=True, max_length=1000)),
                ('average_rating', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5)])),
                ('image', models.ImageField(upload_to='product_images/')),
                ('pdf', models.FileField(upload_to='product_pdfs/')),
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
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('mediaURL', models.URLField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('up_or_down', models.CharField(choices=[('U', 'up'), ('D', 'down')], default=0, max_length=1)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.comment')),
            ],
            options={
                'verbose_name': 'Comment Voting',
                'verbose_name_plural': 'Comment Votings',
                'ordering': ['comment', 'myuser'],
            },
        ),
    ]
