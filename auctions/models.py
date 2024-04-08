from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class AuctionListing(models.Model):
    id = models.BigAutoField(primary_key=True)
    auctioneer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", default=1)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    starting_bid = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=8, default="open")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="auctions")

    def __str__(self):
        return f"\"{self.title}\" by {self.auctioneer}"
    
    
class Bid(models.Model):
    id = models.BigAutoField(primary_key=True)
    bid = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids_made")
    bid_time = models.DateTimeField(auto_now_add=True)
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.bid}$ by {self.bidder} on {self.auction.title}"
    
class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_made")
    comment_time = models.DateTimeField(auto_now_add=True)
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.commenter} commented on {self.auction.title}"
    
class Watchlist(models.Model):
    id = id = models.BigAutoField(primary_key=True)
    watchlist_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_items")
    watchlist_auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watchlist_listings")

