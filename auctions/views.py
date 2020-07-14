from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Comment, Bids, Watchlist


def index(request):
    return render(request, "auctions/index.html",{'listings':Listing.objects.all()})


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

def add_listing(request):
    if request.method=='GET':
        return render(request,"auctions/listings.html")
    else:
        x=request.POST
        l=Listing(title=x['title'],description=x['description'],base_bid=x['base_bid'],url=x['url'],category=x['category'],created_by=request.user)
        l.save()
        return render(request,'auctions/show_message.html',{'message':"Listing created successfully!!!!"})

def list(request,id1):
    if request.method=='GET':
        listing=Listing.objects.filter(id=id1).first()
        watchlist=None
        if(request.user.is_authenticated):
            watchlist =Watchlist.objects.filter(listing=listing,user=request.user).first()
        comment=listing.comment_set.all()
        x=listing.max_bid()
        y=listing.base_bid
        print(x)
        if x['bid__max'] is None:
            x['bid__max']=y
        print(y)
        return render(request,"auctions/list.html",{'listing':listing,'comments':comment,'watchlist':watchlist,'max_bid':x})
def comment(request):
    if request.method=='POST':
        text=request.POST['comment']
        id1=request.POST['id']
        user=request.user
        com=Comment(listing=Listing.objects.filter(id=id1).first(),user=user,text=text)
        com.save()
        return HttpResponseRedirect(reverse('list',kwargs= {'id1':id}))
def add_watch(request,id):
    w=Watchlist(user=request.user,listing=Listing.objects.get(id=id))
    w.save()
    return HttpResponseRedirect(reverse('list',kwargs= {'id1':id}))
def del_watch(request,id):
    w=Watchlist.objects.filter(user=request.user , listing=Listing.objects.get(id=id)).first()
    w.delete()
    return HttpResponseRedirect(reverse('list',kwargs={'id1':id}))
def add_bid(request,id):
    if request.method=='POST':
        bid=request.POST['bid']
        #max_bid=Bids.object.all().filter(listing=Listing.objects.get(pk=id)).aggregate(Max('bid'))
        listing=Listing.objects.get(pk=id)
        b=Bids(listing=Listing.objects.get(pk=id),user=request.user,bid=bid)
        b.save()
        listing.max_bid=b
        listing.winner=b.user
        listing.save()
        return HttpResponseRedirect(reverse('list',kwargs={'id1':id}))

def close_bid(request,id):
    listing=Listing.objects.get(pk=id)
    listing.status=False
    listing.save()
    return HttpResponseRedirect(reverse('list',kwargs={'id1':id}))
def watchlist(request):
    w=Watchlist.objects.filter(user = request.user)
    return render(request,"auctions/watchlist.html",{"watchlist":w})
def categories(request):
    categ=Listing.objects.values('category').distinct()
    #print(categ)
    return render(request,"auctions/categ.html",{'categ':categ})
def category_page(request,name):
    l=Listing.objects.filter(category=name)
    return render(request,"auctions/categ_page.html",{'categ':l})
