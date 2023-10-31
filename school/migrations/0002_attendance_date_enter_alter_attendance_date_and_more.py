# Generated by Django 4.2.4 on 2023-10-30 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='date_enter',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='date_leave',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]