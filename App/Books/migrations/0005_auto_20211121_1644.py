# Generated by Django 3.2.9 on 2021-11-21 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0004_rename_readdata_t_record_readdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_record',
            name='readflag',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='t_record',
            name='thoughts',
            field=models.TextField(blank=True, default=''),
        ),
    ]