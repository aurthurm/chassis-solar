# Generated by Django 3.0.3 on 2020-03-01 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20200222_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariant',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
