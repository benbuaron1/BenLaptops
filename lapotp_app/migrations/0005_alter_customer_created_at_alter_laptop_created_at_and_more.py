# Generated by Django 4.0.2 on 2022-02-23 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lapotp_app', '0004_laptop_memory1_got_laptop_memory2_got_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='laptop',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='manufacurer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='orderitems',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
