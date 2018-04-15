# Generated by Django 2.0.4 on 2018-04-15 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_sms'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='base.Base')),
                ('text', models.TextField()),
                ('related_parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_related_base', to='base.Base')),
            ],
            bases=('base.base',),
        ),
    ]