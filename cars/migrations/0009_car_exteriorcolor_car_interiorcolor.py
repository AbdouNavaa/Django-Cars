# Generated by Django 5.1 on 2024-08-28 21:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0008_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='ExteriorColor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='exterior_color', to='cars.color'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='car',
            name='InteriorColor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='interior_color', to='cars.color'),
            preserve_default=False,
        ),
    ]
