# Generated by Django 2.0.4 on 2018-04-24 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_auto_20180418_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='address',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
