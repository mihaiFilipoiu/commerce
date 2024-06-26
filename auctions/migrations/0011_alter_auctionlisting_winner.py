# Generated by Django 5.0.3 on 2024-04-08 13:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auctionlisting_winner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wins', to=settings.AUTH_USER_MODEL),
        ),
    ]
