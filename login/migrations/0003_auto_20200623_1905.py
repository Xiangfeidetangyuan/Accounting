# Generated by Django 3.0.7 on 2020-06-23 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_expenditem_incomitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='mail',
            field=models.CharField(default=1145902847, max_length=16),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='expenditem',
            name='ItemType',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='incomitem',
            name='ItemType',
            field=models.CharField(max_length=16),
        ),
    ]