# Generated by Django 3.0.4 on 2021-04-11 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20210411_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='gender',
            field=models.IntegerField(choices=[('0', 'Male'), ('1', 'Female')], null=True),
        ),
    ]
