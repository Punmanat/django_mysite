# Generated by Django 2.2 on 2019-04-17 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birthday',
            field=models.DateField(null=True),
        ),
    ]