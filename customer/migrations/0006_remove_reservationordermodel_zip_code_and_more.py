# Generated by Django 4.1.5 on 2023-02-26 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_reservationordermodel_remove_ordermodel_items_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservationordermodel',
            name='zip_code',
        ),
        migrations.AlterField(
            model_name='reservationordermodel',
            name='noOfSeatReserved',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]