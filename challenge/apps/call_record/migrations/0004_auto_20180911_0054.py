# Generated by Django 2.1.1 on 2018-09-11 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('call_record', '0003_auto_20180911_0052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callrecord',
            name='record_type',
            field=models.CharField(choices=[('start', 'Call Start Record'), ('end', 'Call End Record')], default='start', max_length=28, verbose_name='Type'),
        ),
    ]
