# Generated by Django 5.0.1 on 2024-03-25 12:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_user_id', models.IntegerField(null=True, verbose_name='telegram user ID')),
                ('max_query_number', models.IntegerField(default=5, verbose_name='max query number')),
                ('update_period', models.IntegerField(default=0, verbose_name='update period (minutes)')),
                ('type_name', models.CharField(choices=[('registered', 'registered'), ('regular', 'regular'), ('vip', 'vip')], default='registered', max_length=20, verbose_name='user account type name')),
            ],
            options={
                'verbose_name': 'personal_setting',
                'verbose_name_plural': 'personal_settings',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='personal_setting',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='accounts.personalsetting'),
        ),
    ]
