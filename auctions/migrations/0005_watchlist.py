# Generated by Django 4.1.3 on 2024-03-28 18:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auctionlisting_auctioneer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('watchlist_auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist_listings', to='auctions.auctionlisting')),
                ('watchlist_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist_items', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
