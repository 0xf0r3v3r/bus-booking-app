# Generated by Django 4.2.8 on 2023-12-24 07:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trip",
            name="price",
            field=models.IntegerField(verbose_name="Ціна"),
        ),
    ]
