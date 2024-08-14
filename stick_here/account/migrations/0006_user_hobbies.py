# Generated by Django 5.0.8 on 2024-08-08 12:11

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_remove_userprofile_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hobbies',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('기타', '기타'), ('테니스', '테니스'), ('헬스', '헬스'), ('골프', '골프'), ('풋살', '풋살'), ('축구', '축구'), ('수영', '수영'), ('요리', '요리'), ('농구', '농구'), ('야구', '야구'), ('독서', '독서'), ('탁구', '탁구'), ('양궁', '양궁'), ('사격', '사격'), ('프라모델', '프라모델')], default='기타', max_length=47, null=True, verbose_name='취미'),
        ),
    ]
