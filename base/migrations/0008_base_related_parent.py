# Generated by Django 2.0.4 on 2018-05-16 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_topfilter'),
    ]

    operations = [
        migrations.AddField(
            model_name='base',
            name='related_parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_parent_name', to='base.Base'),
        ),
    ]
