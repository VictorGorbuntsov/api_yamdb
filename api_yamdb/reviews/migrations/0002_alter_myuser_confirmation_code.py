# Generated by Django 3.2 on 2023-07-11 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=300, verbose_name='Код входа'),
        ),
    ]