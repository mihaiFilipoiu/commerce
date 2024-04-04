from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:auction_id>/", views.listing_view, name="listing_view"),
    path("toggle_watchlist/<int:auction_id>/", views.toggle_watchlist, name="toggle_watchlist"),
    path("watchlist", views.watchlist_view, name="watchlist_view")
]
