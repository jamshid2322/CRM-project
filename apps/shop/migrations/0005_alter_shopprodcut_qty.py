# Generated by Django 4.2.1 on 2023-06-05 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_shopprodcut'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopprodcut',
            name='qty',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
