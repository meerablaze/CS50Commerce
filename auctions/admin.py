from django.contrib import admin

# Register your models here.
from .models import User, Listing, Comment, Bids, Watchlist

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bids)
admin.site.register(Watchlist)
