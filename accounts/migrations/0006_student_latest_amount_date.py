# Generated by Django 4.2.4 on 2023-09-12 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_student_amount_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='latest_amount_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
