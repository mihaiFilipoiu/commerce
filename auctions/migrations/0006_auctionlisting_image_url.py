# Generated by Django 5.0.3 on 2024-04-07 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]