# Generated by Django 4.2.4 on 2023-09-14 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_alter_each_pay_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finance',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]