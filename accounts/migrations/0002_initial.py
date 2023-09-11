# Generated by Django 4.2.4 on 2023-09-11 15:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('accounts', '0001_initial'),
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='sciences',
            field=models.ManyToManyField(blank=True, related_name='teachers', to='school.science', verbose_name='Fanlar:'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='student',
            name='class_of_school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='school.class'),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='parent',
            name='children',
            field=models.ManyToManyField(blank=True, related_name='parents', to='accounts.student'),
        ),
        migrations.AddField(
            model_name='parent',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='employer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='admin',
            name='permissions',
            field=models.ManyToManyField(blank=True, related_name='admins', to='accounts.permission', verbose_name='Ruxsatnomalar:'),
        ),
        migrations.AddField(
            model_name='admin',
            name='types',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admins', to='accounts.type_of_admin', verbose_name='Admin turi:'),
        ),
        migrations.AddField(
            model_name='admin',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='admin', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
