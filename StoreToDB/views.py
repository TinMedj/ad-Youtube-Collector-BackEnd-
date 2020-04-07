# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from hashlib import sha512
from models import user
from models import adReason
from models import hostingVideo
from models import youtubeAds
from models import videoAd
from models import FloatingAd
from models import index
from django.views.decorators.csrf import csrf_exempt
import django
import logging
import json
import unicodedata
#from django.http import JsonResponse
from django.http import HttpResponse
JsonResponse = lambda response: HttpResponse(json.dumps(response), content_type="application/json")
version = django.VERSION
if (version[0] >= 1) and (version[1] >= 7):
    import django.http

    JsonResponse = django.http.JsonResponse

import datetime

# create an instance of logger 
logger = logging.getLogger(__name__)

STATUS = 'status'
FAILURE = 'failure'
SUCCESS = 'success'
REASON = 'reason'
POST_REQUEST = 'this request should be a POST one'
NOT_CONNECTED_USER = 'the user is not connected we don"t handle this'
AD_LINK = 'ad_link'
USER_ID = 'user_id'
TYPE = 'type'
SOMETHING_WRONG = "there were something wrong with your request please review it "




def addReason(data,ads):
    for i in data["ad_reasons"]:
        print'i {}'.format(i)
        chaine = unicodedata.normalize('NFKD', i).encode('ascii', 'ignore')
        id_Reason = sha512(str(chaine)).hexdigest()
        reason = adReason(id=id_Reason,title = i)
        reason.save()
        ads.reasons.add(reason)


@csrf_exempt
def store_Data_To_DataBase(request):
    response = {}
    print 'We entered the function'
    logger.info("Excecuting ")  
    print 'We started the function'
        #we test if it's a post request 
    if request.method!='POST':
        response[STATUS] = FAILURE
        response[REASON] = POST_REQUEST
        print'there is no post method'
        return JsonResponse(response)
    print'here we go'
    body = request.body.decode('utf-8')
    json_data = json.loads(body)
    print'json data {}'.format(json_data["connected"])
        
        #we have the user 
        #we test first if the user is connected on his gmail account while watching youtube videos 
         #we extract the user information
    if json_data["connected"] == False :
        user_id = sha512(str(json_data["user"]["id"]+json_data["country"])).hexdigest()
        user_name = json_data["user"]["name"]+json_data["country"]
        user_email = json_data["user"]["email"]+json_data["country"]
    else:
        user_id = sha512(str(json_data["user"]["id"])).hexdigest()
        user_name = json_data["user"]["name"]
        user_email = json_data["user"]["email"]
    user_country = json_data["country"]
    u = user(id=user_id,
                  user_name= user_name,
                  user_email = user_email,
                  country = user_country
         )
    u.save()
    print 'We saved the user'
    logger.info(' the user is saved')
    indexForUser = index(id = user_id,
                              user_id = json_data["user"]["id"],
                              user_name = user_name)
    indexForUser.save()  
    print 'We saved the user'
    logger.info(': the index of user is saved')                   
       

         #we extract the host video information 

    video_name = json_data["host_video"]["name"]
    video_link = json_data["host_video"]["link"]
    video_date = json_data["host_video"]["date"]
    nbr_vues = json_data["host_video"]["total_views"]
    channel_name = json_data["host_video"]["channel_name"]
    channel_link = json_data["host_video"]["channel_link"]
    channel_img  = json_data["host_video"]["channel_img"]
    nbr_followers = json_data["host_video"]["nbr_followers"] 
    channel_description = json_data["host_video"]["channel_description"]
        
    logger.info(': we extracted the vide host')
    videoHost = hostingVideo(
                name = video_name,
                link = video_link,
                date = video_date,
                nbr_views =nbr_vues,
                channel_name =channel_name, 
                channel_link = channel_link,
                channel_img = channel_img,
                channel_description = channel_description,
                nbr_followers = nbr_followers
                )
    videoHost.save()
    logger.info(' video host is saved')
    u.videos.add(videoHost) 
    logger.info(': the video is added to user')
    print 'We saved the video host and we connceted it with the user'
    if json_data["ad_or_not"]==True:
             #this a video ad 
        print'this is a video'
        logger.info(': this is a video ad')
        type_ad ='V'
        link = json_data["ad"]["ad_link"]
        advertiser_name = json_data["ad"]["advertiser_name"]
        ad_channel_description = json_data["ad"]["ad_channel_description"]
        ad_channel_name = json_data["ad"]["ad_channel_name"]
        ad_channel_link = json_data["ad"]["ad_channel_link"]
        ad_channel_img  = json_data["ad"]["ad_channel_img"]
        ad_page_img     = json_data["ad"]["ad_page_img"]
        ad_page_desctiption = json_data["ad"]["ad_page_desctiption"]
        ad_page_link = json_data["ad"]["ad_page_link"]
        skeept_or_not = json_data["ad"]["skeept_or_not"]
        advertiser_checked_or_not = json_data["ad"]["checked_or_not"]
        reason_cheked = json_data["ad"]["reason_cheked"]
        channel_cheked = json_data["ad"]["channel_cheked"]
        time = datetime.datetime.now()
        response[AD_LINK] = link
        logger.info(': the ad was saved')
        print 'We cllected a video ad'
        videoAdInstance = videoAd(typeAd = type_ad,
                    time = time,     
                    link = link,
                    advertiser_name = advertiser_name,
                    ad_channel_description = ad_channel_description,
                    ad_channel_name = ad_channel_name,
                    ad_channel_link = ad_channel_link,
                    ad_channel_img  = ad_channel_img,
                    ad_page_img     = ad_page_img,
                    ad_page_desctiption = ad_page_desctiption,
                    ad_page_link = ad_page_link,
                    ad_skeept_or_not = skeept_or_not,
                    advertiser_checked_or_not = advertiser_checked_or_not,
                    reason_cheked = reason_cheked,
                    channel_checked = channel_cheked
                    )
        videoAdInstance.save()
        videoAdInstance.users.add(u)
        addReason(json_data,videoAdInstance)
        print 'We saved the video Ad'
        logger.info(': the videoAd was saved')

    if json_data["ad_or_not"]==False:
            #this video is a float card
        print 'this is a float card ad'
        response[AD_LINK] = "there is no link" 
        type_ad ='F'
        title = json_data["ad_floating"]["title"][0]+' '+json_data["ad_floating"]["title"][1]
        description = json_data["ad_floating"]["description"][0]+' '+json_data["ad_floating"]["description"][1]
        linkToURL = json_data["ad_floating"]["link"]
        link = ""
        for i in linkToURL:
            if i != "":
                link = i +', '
 
        img = json_data["ad_floating"]["img"]
        ad_reason_cheked = json_data["ad_floating"]["ad_reason_cheked"]
        ad_removed = json_data["ad_floating"]["ad_removed"]
        time = datetime.datetime.now()
        print'img{}'.format(img)
        print'channel img{}'.format(channel_img)
        floatAd = FloatingAd(typeAd = type_ad,
                time = time,
                title = title,
                description = description,
                link = link,
                img = img,
                ad_reason_cheked = ad_reason_cheked,
                ad_removed = ad_removed
            )
        floatAd.save()
        floatAd.users.add(u)
        addReason(json_data,floatAd)
        print 'We saved the float ad'
        
    response[USER_ID] = user_id
    response[TYPE] = type_ad

    return JsonResponse(response)




    

        

        


