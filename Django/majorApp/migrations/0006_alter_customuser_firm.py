# Generated by Django 5.2 on 2025-05-04 04:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('majorApp', '0005_alter_customuser_firm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='firm',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='majorApp.firm'),
        ),
    ]
