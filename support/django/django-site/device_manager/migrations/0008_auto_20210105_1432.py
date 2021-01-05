# Generated by Django 3.0.2 on 2021-01-05 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device_manager', '0007_auto_20210105_1004'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Device',
        ),
        migrations.AlterModelOptions(
            name='fleet',
            options={'verbose_name_plural': 'fleet middleware'},
        ),
        migrations.AddField(
            model_name='receiveddata',
            name='owner',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]