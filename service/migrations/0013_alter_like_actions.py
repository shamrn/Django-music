# Generated by Django 3.2.4 on 2021-06-09 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0012_auto_20210608_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='actions',
            field=models.CharField(blank=True, choices=[('like', 'like'), ('dislike', 'dislike')], max_length=50, null=True),
        ),
    ]
