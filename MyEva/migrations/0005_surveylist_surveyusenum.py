# Generated by Django 2.1.1 on 2019-03-18 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyEva', '0004_auto_20190317_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveylist',
            name='SurveyUseNum',
            field=models.IntegerField(default=0),
        ),
    ]