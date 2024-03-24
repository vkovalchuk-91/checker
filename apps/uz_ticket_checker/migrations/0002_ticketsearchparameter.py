# Generated by Django 5.0.1 on 2024-03-23 22:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_baseparameter_parametercategory_checkertask_and_more'),
        ('uz_ticket_checker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketSearchParameter',
            fields=[
                ('baseparameter_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounts.baseparameter')),
                ('start_date', models.DateTimeField(verbose_name='start date')),
                ('end_date', models.DateTimeField(verbose_name='end date')),
                ('arrival_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrivals', to='uz_ticket_checker.station', verbose_name='arrival station')),
                ('departure_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departures', to='uz_ticket_checker.station', verbose_name='departure station')),
                ('seat_type', models.ManyToManyField(to='uz_ticket_checker.seattype')),
                ('train_number', models.ManyToManyField(to='uz_ticket_checker.trainnumber')),
                ('wagon_type', models.ManyToManyField(to='uz_ticket_checker.wagontype')),
            ],
            bases=('accounts.baseparameter',),
        ),
    ]
