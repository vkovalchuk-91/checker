# Generated by Django 5.0.1 on 2024-04-03 20:41

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckerTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created date')),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='updated date')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_delete', models.BooleanField(default=False, verbose_name='delete')),
                ('update_period', models.IntegerField(default=5, verbose_name='update period (minutes)')),
                ('task_param', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checker_task_parameters', to='accounts.baseparameter', verbose_name='checker task parameters')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checker_tasks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'checker_task',
                'verbose_name_plural': 'checker_tasks',
            },
        ),
    ]
