from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class AuctionListing(models.Model):
    id = models.BigAutoField(primary_key=True)
    auctioneer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", default=1)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    starting_bid = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="auctions")

    def __str__(self):
        return f"\"{self.title}\" by {self.auctioneer}"
    
    
class Bid(models.Model):
    id = models.BigAutoField(primary_key=True)
    bid = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids_made")
    bid_time = models.DateTimeField(auto_now_add=True)
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")

class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_made")
    comment_time = models.DateTimeField(auto_now_add=True)
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")

