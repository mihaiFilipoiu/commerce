from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.urls import reverse

from .models import User, AuctionListing, Watchlist, Category, Bid, Comment
from .forms import CreateListingForm, BidForm, CommentForm

def index(request):
    auctions = AuctionListing.objects.annotate(
        highest_bid=Max("bids__bid")
    ).order_by("-date_created")
    return render(request, "auctions/index.html", {
        "auctions": auctions
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == "POST": # POST
        form = CreateListingForm(request.POST)
        if form.is_valid():
            auction_listing = form.save(commit=False)
            auction_listing.auctioneer = request.user 
            auction_listing.save()
            return HttpResponseRedirect(reverse("index"))
    else: # GET
        return render(request, "auctions/create_listing.html", {
            "form": CreateListingForm
        })

def listing_view(request, auction_id):
    # GET
    auction = AuctionListing.objects.get(pk=auction_id)
    if request.user.is_authenticated:
        is_in_watchlist = Watchlist.objects.filter(watchlist_user=request.user, watchlist_auction=auction).exists()
    else:
        is_in_watchlist = False
    
    current_bid = auction.bids.order_by('-bid').first()
    if current_bid:
        current_bid_price = current_bid.bid
    else:
        current_bid_price = 0

    return render(request, "auctions/listing_page.html", {
        "auction": auction,
        "is_in_watchlist": is_in_watchlist,
        "form": BidForm,
        "comment_form": CommentForm,
        "comments": auction.comments.all().order_by('-comment_time'),
        "current_bid": current_bid_price
    })

@login_required
def toggle_watchlist(request, auction_id):
    if request.method == "POST": # POST
        auction = auction = AuctionListing.objects.get(pk=auction_id)
        watchlist_item, created_now = Watchlist.objects.get_or_create(watchlist_user=request.user, watchlist_auction=auction)
        if not created_now:
            watchlist_item.delete()
        return HttpResponseRedirect(reverse('listing_view', args=[auction_id]))

@login_required
def watchlist_view(request):
    watchlist_items = Watchlist.objects.filter(watchlist_user=request.user).order_by("id")
    return render(request, "auctions/watchlist.html", {
        "watchlist_items": watchlist_items
    })

@login_required
def place_bid(request, auction_id):
    auction = AuctionListing.objects.get(pk=auction_id)

    if request.method == "POST": # POST
        form = BidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data['bid']
            if bid_amount >= auction.starting_bid:
                highest_bid = auction.bids.order_by('-bid').first()
                if not highest_bid or bid_amount > highest_bid.bid:
                    bid = form.save(commit=False)
                    bid.auction = auction
                    bid.bidder = request.user
                    bid.save()
                    messages.success(request, "Bid placed succesfully.")
                else:
                    messages.error(request, "Your bid must be higher than the current highest bid.")
            else:
                messages.error(request, "Your bid must be higher or equal than the starting bid.")
        
        return HttpResponseRedirect(reverse('listing_view', args=[auction_id]))
    

def add_comment(request, auction_id):
    auction = AuctionListing.objects.get(pk=auction_id)

    if request.method == "POST": # POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.auction = auction
            comment.commenter = request.user
            comment.save()
            return HttpResponseRedirect(reverse('listing_view', args=[auction_id]))
        
def category_view(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category_page(request, category_id):
    category = Category.objects.get(pk=category_id)
    auctions = AuctionListing.objects.filter(category=category).annotate(
        highest_bid=Max("bids__bid")
    ).order_by("-date_created")
    
    return render(request, "auctions/category.html", {
        "category": category,
        "auctions": auctions
    })
