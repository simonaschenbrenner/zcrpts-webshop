# Generated by Django 3.2.9 on 2022-01-10 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0008_alter_vote_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('up_or_down', 'comment')},
        ),
        migrations.DeleteModel(
            name='Flag',
        ),
    ]
