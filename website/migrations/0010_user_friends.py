# Generated by Django 2.2.26 on 2022-07-19 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_auto_20220719_0112'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='friends',
            field=models.TextField(blank=True),
        ),
    ]
