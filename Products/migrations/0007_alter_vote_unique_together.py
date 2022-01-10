# Generated by Django 3.2.9 on 2022-01-03 22:39

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Products', '0006_alter_comment_is_flagged'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('up_or_down', 'myuser', 'comment')},
        ),
    ]
