# Generated by Django 3.2.7 on 2021-09-13 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20210913_0857'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='image',
        ),
        migrations.AddField(
            model_name='products',
            name='imageUrl',
            field=models.URLField(blank=True, null=True),
        ),
    ]
