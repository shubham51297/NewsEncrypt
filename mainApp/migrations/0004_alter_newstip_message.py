# Generated by Django 4.0.3 on 2022-05-09 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0003_source_privatekey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newstip',
            name='message',
            field=models.BinaryField(),
        ),
    ]
