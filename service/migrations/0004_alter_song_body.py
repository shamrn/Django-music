# Generated by Django 3.2.4 on 2021-06-04 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_auto_20210604_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
    ]
