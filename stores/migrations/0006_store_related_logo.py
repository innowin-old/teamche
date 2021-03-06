# Generated by Django 2.0.4 on 2018-05-03 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_topfilter'),
        ('stores', '0005_store_active_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='related_logo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='store_related_logo_name', to='base.File'),
        ),
    ]
