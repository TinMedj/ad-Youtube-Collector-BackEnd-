# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.



#in this model we will define the tables of our application 

class adReason(models.Model):
    id = models.CharField(max_length=128,primary_key = True)
    title = models.CharField(max_length=500)


class hostingVideo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=400)
    link = models.CharField(max_length=200)
    date = models.CharField(max_length=40)
    nbr_views = models.CharField(max_length=30)
    channel_name = models.CharField(max_length=100)
    channel_link = models.CharField(max_length=200)
    channel_img = models.CharField(max_length=500)
    channel_description = models.TextField(blank=True, null=True)
    nbr_followers = models.CharField(max_length=50)
    


class user(models.Model):
    id = models.CharField(max_length=128,primary_key = True)
    user_name = models.CharField(max_length=100)
    user_email = models.CharField(max_length=100)
    videos = models.ManyToManyField(hostingVideo)


class youtubeAds(models.Model):
    class Meta:
        abstract = True
    TYPE_ADS = (
        ('V', 'VIDEO AD'),
        ('F', 'FLOATING CARD ADS '),
    )
    
    id = models.AutoField(primary_key=True)
    typeAd = models.CharField(max_length=1, choices = TYPE_ADS )
    reasons = models.ManyToManyField(adReason)
    time = models.DateField()
    users = models.ManyToManyField(user)


class videoAd(youtubeAds):
     
     link = models.CharField(max_length=400)
     advertiser_name = models.CharField(max_length=100)
     ad_channel_description = models.TextField(blank=True, null=True)
     ad_channel_name = models.CharField(max_length=100)
     ad_channel_link = models.CharField(max_length=200)
     ad_channel_img  = models.CharField(max_length=400)
     ad_page_img     = models.CharField(max_length=400)
     ad_page_desctiption = models.TextField(blank=True, null=True)
     ad_page_link = models.CharField(max_length=200)
     ad_skeept_or_not = models.BooleanField(default=False)
     advertiser_checked_or_not = models.BooleanField(default=False)
     reason_cheked = models.BooleanField(default=False)
     channel_checked = models.BooleanField(default=False)
     

 
class FloatingAd(youtubeAds):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    img = models.CharField(max_length=300)
    ad_reason_cheked = models.BooleanField(default=False)
    ad_removed = models.BooleanField(default=False)
    

class index(models.Model):
    id = models.CharField(max_length=128,primary_key = True)
    user_id = models.CharField(max_length=200,unique = True)
    user_name = models.CharField(max_length=200)
    