# Generated by Django 2.0.4 on 2018-05-16 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20180426_0926'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='active_flag',
            field=models.BooleanField(default=False),
        ),
    ]
