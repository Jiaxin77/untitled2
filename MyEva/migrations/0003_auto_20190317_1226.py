# Generated by Django 2.1.1 on 2019-03-17 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyEva', '0002_auto_20190314_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlist',
            name='UserId',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
