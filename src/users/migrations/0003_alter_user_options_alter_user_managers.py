# Generated by Django 4.2.4 on 2023-08-26 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_last_activity_user__last_activity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('username',), 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
    ]
