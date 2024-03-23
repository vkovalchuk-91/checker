# Generated by Django 5.0.1 on 2024-03-10 21:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccountType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='user account type name')),
                ('max_query_number', models.IntegerField(default=0, verbose_name='max query number')),
                ('update_period', models.IntegerField(default=0, verbose_name='update period (minutes)')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='telegram_user_id',
            field=models.IntegerField(default=0, verbose_name='telegram user ID'),
        ),
        migrations.AddField(
            model_name='user',
            name='update_period',
            field=models.IntegerField(default=0, verbose_name='update period (minutes)'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_account_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_account_type', to='accounts.useraccounttype', verbose_name='user account type'),
        ),
    ]
