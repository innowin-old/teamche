# Generated by Django 2.0.4 on 2018-04-30 14:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0007_topfilter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='base.Base')),
                ('title', models.CharField(max_length=50)),
                ('text', models.TextField()),
                ('post_related_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_related_user_name', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('base.base',),
        ),
    ]
