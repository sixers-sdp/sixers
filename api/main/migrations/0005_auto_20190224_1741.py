# Generated by Django 2.1.5 on 2019-02-24 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20190223_2021'),
    ]

    operations = [
        migrations.RenameField(
            model_name='executionplan',
            old_name='plan',
            new_name='plan_out',
        ),
        migrations.AddField(
            model_name='executionplan',
            name='plan_parsed',
            field=models.TextField(null=True),
        ),
    ]
