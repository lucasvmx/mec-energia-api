# Generated by Django 4.1 on 2022-12-08 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='type',
            field=models.CharField(editable=False, max_length=25),
        ),
    ]