# Generated by Django 3.2.4 on 2021-06-07 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0008_auto_20210607_0900'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='song',
            options={'ordering': ('-date_created',)},
        ),
        migrations.AddField(
            model_name='song',
            name='link_sound',
            field=models.TextField(default='null'),
            preserve_default=False,
        ),
    ]