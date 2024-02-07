# Generated by Django 4.2.8 on 2024-02-07 08:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Користувач",
            ),
        ),
        migrations.AddField(
            model_name="station",
            name="city",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.city",
                verbose_name="Місто",
            ),
        ),
        migrations.AddField(
            model_name="partner",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="core.company",
                verbose_name="Компанія",
            ),
        ),
        migrations.AddField(
            model_name="partner",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Користувач",
            ),
        ),
        migrations.AddField(
            model_name="bus",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="core.company",
                verbose_name="Компанія",
            ),
        ),
    ]
