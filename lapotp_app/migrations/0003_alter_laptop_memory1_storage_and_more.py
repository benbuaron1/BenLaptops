# Generated by Django 4.0.2 on 2022-02-23 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lapotp_app', '0002_order_order_laptops_alter_customer_table_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laptop',
            name='memory1_storage',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='memory1_type',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]