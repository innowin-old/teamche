# Generated by Django 2.0.4 on 2018-06-08 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_base_updated_by_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='base',
            name='updated_by_user',
        ),
        migrations.AddField(
            model_name='base',
            name='is_new',
            field=models.BooleanField(db_index=True, default=False, help_text='Boolean'),
        ),
    ]
