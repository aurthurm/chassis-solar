# Generated by Django 3.0.3 on 2020-02-09 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_product_product_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producttype',
            name='weight',
            field=models.CharField(max_length=20),
        ),
    ]
