# Generated by Django 2.2.5 on 2019-10-11 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='主键'),
        ),
        migrations.AlterModelTable(
            name='user',
            table='server_user',
        ),
    ]