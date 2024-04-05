from django import forms
from .models import AuctionListing, Bid

class CreateListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ["title", "description", "starting_bid", "category"]

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["bid"]

