# Generated by Django 2.1.1 on 2019-04-23 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyEva', '0002_userlist_searchhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='indexlist',
            name='HeuRegular',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
