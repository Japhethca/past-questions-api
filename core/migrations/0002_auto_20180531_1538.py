# Generated by Django 2.0.5 on 2018-05-31 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_squashed_0004_auto_20180529_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
