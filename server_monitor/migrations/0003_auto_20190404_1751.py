# Generated by Django 2.1.7 on 2019-04-04 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server_monitor', '0002_auto_20190404_0943'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='server',
            unique_together={('server_name', 'server_ip')},
        ),
    ]