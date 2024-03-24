# Generated by Django 5.0.1 on 2024-03-10 22:16

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='country name')),
            ],
        ),
        migrations.CreateModel(
            name='SeatType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_type', models.CharField(max_length=50, verbose_name='seat type')),
            ],
        ),
        migrations.CreateModel(
            name='TrainNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('train_number', models.CharField(max_length=50, verbose_name='train number')),
            ],
        ),
        migrations.CreateModel(
            name='WagonType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wagon_type', models.CharField(max_length=50, verbose_name='wagon type')),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('express_3_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='EXPRESS-3 ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created date')),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='updated date')),
                ('name', models.CharField(max_length=150, verbose_name='station name')),
                ('weight', models.DecimalField(decimal_places=1, max_digits=4, verbose_name='weight')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active.Unselect this instead of deleting accounts.', verbose_name='active')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='country', to='uz_ticket_checker.country', verbose_name='country')),
            ],
            options={
                'verbose_name': 'station',
                'verbose_name_plural': 'stations',
            },
        ),
    ]
