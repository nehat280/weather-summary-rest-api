# Generated by Django 4.2.2 on 2023-06-08 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_scrapper', '0006_alter_weatherdata_apr_alter_weatherdata_aug_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='weatherdata',
            unique_together={('region', 'parameter', 'year')},
        ),
    ]