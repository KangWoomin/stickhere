# Generated by Django 5.0.8 on 2024-08-14 10:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_remove_hobbycategory_골프_remove_hobbycategory_기타_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='textboard',
            name='hobby_category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='account.hobbycategory'),
            preserve_default=False,
        ),
    ]
