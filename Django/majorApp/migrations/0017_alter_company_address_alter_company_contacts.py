# Generated by Django 5.2 on 2025-05-06 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('majorApp', '0016_alter_lead_last_contact_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='contacts',
            field=models.ManyToManyField(blank=True, null=True, to='majorApp.contact'),
        ),
    ]
