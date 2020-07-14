from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.db.models import Max

class User(AbstractUser):
    pass

class Listing(models.Model):
    title      =models.CharField(max_length=200)
    description=models.CharField(max_length=4000)
    base_bid   =models.IntegerField()
    url        =models.URLField(max_length=4000, blank=True)
    category   =models.CharField(null=True, max_length=4000)
    created_by =models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='created_by')
    status =models.BooleanField(default=True)
    winner=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='winner')
    def max_bid(self):
        return Bids.objects.all().filter(listing=self).aggregate(Max('bid'))
    def __str__(self):
        return f"{self.title}-{self.description}-{self.base_bid}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE)
    user    = models.ForeignKey(User,on_delete=models.CASCADE)
    text    = models.CharField(max_length=4000)

    def __str__(self):
        return  f"{self.text}"

class Bids(models.Model):
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE)
    user    = models.ForeignKey(User,on_delete=models.CASCADE)
    bid     = models.IntegerField()

class Watchlist(models.Model):
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE)
    user    = models.ForeignKey(User,on_delete=models.CASCADE)
