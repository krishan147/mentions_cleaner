# -*- coding: utf-8 -*-
import time
import json
import urllib2
import datetime
import pyodbc
import timeit
import sys
import logging
import timeit
import gspread
import os
start = timeit.default_timer()
str_logging_time = str(datetime.datetime.now())
time_start = datetime.datetime.now()
from oauth2client.service_account import ServiceAccountCredentials

time_now = datetime.datetime.now()
convert_time_now = str(time_now).split(".",1)[0]
date_now_unix = time.mktime(datetime.datetime.strptime(convert_time_now, "%Y-%m-%d %H:%M:%S").timetuple())
print date_now_unix

### WRITING TO GOOGLE SHEET

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('ENTER PROJECT NAME HERE', scope)
gc = gspread.authorize(credentials)
wks = gc.open("INSERT GOOGLE SHEET NAME").sheet1
wks.update_acell('A47', 'Running...')
wks.update_acell('B48', 'Will populate when process is finished')
wks.update_acell('B49', 'Will populate when process is finished')
wks.update_acell('B50', 'Will populate when process is finished')
wks.update_acell('B51', 'Will populate when process is finished')
wks.update_acell('B52', 'Will populate when process is finished')
wks.update_acell('B53', 'Will populate when process is finished')
wks.update_acell('D47', '')
wks.update_acell('E47', '')

# CONNECTS TO DB

brpmen = 'DRIVER={SQL Server};SERVER=ENTER SERVER NAME;DATABASE=ENTER DATABASE NAME;UID=ENTER USER ID;PWD=ENTER PASSWORD'
outputs = 'DRIVER={SQL Server};SERVER=ENTER SERVER NAME;DATABASE=ENTER DATABASE NAME;UID=ENTER USER ID;PWD=ENTER PASSWORD'

brpmen_posts = 'ENTER TABLE NAME'
brpmen_terms_two = 'ENTER TABLE NAME''
brpmen_posts_clean = 'ENTER TABLE NAME'
brpmen_dc = 'ENTER TABLE NAME'

### GET TOTAL NUMBER OF FACEBOOK ON THE SYSTEM BEFORE THE PROCESS BEGAN

cnxn = pyodbc.connect(amvbbdo_outputs)
cursor = cnxn.cursor()
cursor.execute("SELECT unique_id FROM "+brpmen_posts_clean+ " ORDER BY unique_id ASC")
rows = cursor.fetchall()
cnxn.close()

num_of_posts_before_running_script = 0
for item in rows:
    if "None" in str(item):
        pass
    else:
        num_of_posts_before_running_script = num_of_posts_before_running_script + 1

str_num_of_posts_before_running_script = str(num_of_posts_before_running_script)

#PULLS DUPLICATES IN ORDER TO BE COMPARED WITH DIRTY DATA

list_dc = []

cnxn = pyodbc.connect(outputs)
cursor = cnxn.cursor()
cursor.execute("SELECT fb_post_id, tw_tweet_id, instagram_media_id FROM "+brpmen_dc)
rows_dc = cursor.fetchall()

for data_dc in rows_dc:
    list_dc.append(data_dc)
        
#PULLS QUERIES
num_of_new_posts = 0
cnxn2 = pyodbc.connect(outputs)
cursor2 = cnxn2.cursor()
cursor2.execute("SELECT brand, term, syntax FROM "+brpmen_terms_two + " ORDER BY term ASC")
rows2 = cursor2.fetchall()
for data2 in rows2:
    if data2:
        terms_brand = data2[0]
        terms_term = data2[1]
        terms_syntax = data2[2]

        print terms_brand, terms_term, terms_syntax

#PULLS CLEAN DATA FROM DIRTY DATA

        cnxn = pyodbc.connect(brpmen)
        cursor = cnxn.cursor()
        cursor.execute("SELECT unique_id, facebook_id, twitter_handle, fb_post_id, tw_tweet_id, location, venue_name, post, tweet, date_posted, country, date_added, instagram_user_id, instagram_user_followers, instagram_user_link, instagram_media_id, instagram_image_text, instagram_comment_count, instagram_like_count, instagram_direct_image_link, instagram_image_description, instagram_handle, instagram_image_link, tw_id, twitter_followers, google_logo_description, source, flag, fb_page_likes, unique_id, fb_url, tw_url  FROM "+brpmen_posts + " WHERE " + terms_syntax)
        rows = cursor.fetchall()
        for data in rows:
            if data:
                clean_unique_id = data[0]
                clean_facebook_id = data[1]
                clean_twitter_handle = data[2]
                clean_fb_post_id = data[3]
                clean_tw_tweet_id = data[4]
                clean_location = data[5]
                clean_venue_name = data[6]
                clean_post = data[7]
                clean_tweet = data[8]
                clean_date_posted = data[9]
                clean_country = data[10]
                clean_date_added = data[11]
                clean_instagram_user_id = data[12]
                clean_instagram_user_followers = data[13]
                clean_instagram_user_link = data[14]
                clean_instagram_media_id = data[15]
                clean_instagram_image_text = data[16]
                clean_instagram_comment_count = data[17]
                clean_instagram_like_count = data[18]
                clean_instagram_direct_image_link = data[19]
                clean_instagram_image_description = data[20]
                clean_instagram_handle = data[21]
                clean_instagram_image_link = data[22]
                clean_tw_id = data[23]
                clean_twitter_followers = data[24]
                clean_google_logo_description = data[25]
                clean_source = data[26]
                clean_flag = data[27]
                clean_fb_page_likes = data[28]
                brpmen_posts_unique_id = data[29]
                fb_url = data[30]
                tw_url = data[31]

                source = "brpmen"

                clean_date_posted_unix = time.mktime(datetime.datetime.strptime(str(clean_date_posted), "%Y-%m-%d %H:%M:%S").timetuple())
                str_date_posted = str(clean_date_posted).split(".",1)[0]
                date_posted_unix = time.mktime(datetime.datetime.strptime(str_date_posted, "%Y-%m-%d %H:%M:%S").timetuple())

                year_timestamp = 31591981
                day_timestamp = 41210
                time_then = date_comparison_now - day_timestamp 

                if date_posted_unix > time_then: 

#CHECK IF WE HAVE ANY DUPLICATES AND DROPS DATA INTO THE CLEAN TABLE AND BRPMEN DUPLICATE CHECKER TABLE
                
                    if str(clean_fb_post_id) not in str(list_dc):
                        #print clean_fb_post_id
                        
                        cnxn = pyodbc.connect(outputs)
                        cursor = cnxn.cursor()
                        cursor.execute("INSERT INTO "+brpmen_dc+" (fb_post_id) values(?)",clean_fb_post_id)
                        cnxn.commit()
                           
                        cnxn = pyodbc.connect(outputs)
                        cursor = cnxn.cursor()
                        cursor.execute("INSERT INTO "+brpmen_posts_clean+" (facebook_id, fb_post_id, location, venue_name, post, date_posted, country, date_added, fb_page_likes,brand,term,brpmen_unique_id,source,fb_url) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",clean_facebook_id, clean_fb_post_id,clean_location,clean_venue_name,clean_post,clean_date_posted,clean_country,clean_date_added,clean_fb_page_likes, terms_brand, terms_term, brpmen_posts_unique_id,source,fb_url)
                        cnxn.commit()
                        num_of_new_posts = num_of_new_posts + 1
                        print "inserted new facebook post!"

                    if str(clean_fb_post_id) in str(list_dc):
                        pass
                        #print "we already have this facebook post!"
                       
                    if str(clean_tw_tweet_id) not in str(list_dc):
                        #print clean_tw_tweet_id
                                
                        cnxn = pyodbc.connect(outputs)
                        cursor = cnxn.cursor()
                        cursor.execute("INSERT INTO "+brpmen_dc+" (tw_tweet_id) values(?)",clean_tw_tweet_id)
                        cnxn.commit()

                        cnxn = pyodbc.connect(outputs)
                        cursor = cnxn.cursor()
                        cursor.execute("INSERT INTO "+brpmen_posts_clean+" (twitter_handle, tw_tweet_id, location, venue_name, tweet, date_posted, country, date_added, tw_id, twitter_followers,brand,term,brpmen_unique_id,source,tw_url) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", clean_twitter_handle, clean_tw_tweet_id,clean_location,clean_venue_name,clean_tweet,clean_date_posted,clean_country,clean_date_added,clean_tw_id,clean_twitter_followers,terms_brand, terms_term, brpmen_posts_unique_id,source,tw_url)
                        cnxn.commit()
                        num_of_new_posts = num_of_new_posts + 1
                        print "inserted new tweet!"

                    if str(clean_tw_tweet_id) in str(list_dc):
                        pass
                        #print "we already have this tweet!"
                               
                    if str(clean_instagram_media_id) not in str(list_dc):
                        print clean_instagram_media_id
                        
##                        cnxn = pyodbc.connect(amvbbdo_outputs)
##                        cursor = cnxn.cursor()
##                        cursor.execute("INSERT INTO "+brpmen_dc+" (instagram_media_id) values(?)",clean_instagram_media_id)
##                        cnxn.commit()
##                        
##                        cnxn = pyodbc.connect(amvbbdo_outputs)
##                        cursor = cnxn.cursor()
##                        cursor.execute("INSERT INTO "+brpmen_posts_clean+" (location, venue_name,date_posted, country, date_added, instagram_user_id, instagram_user_followers, instagram_user_link, instagram_media_id, instagram_image_text, instagram_comment_count, instagram_like_count, instagram_direct_image_link, instagram_image_description, instagram_handle, instagram_image_link,brand,term,brpmen_unique_id,source) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",clean_location,clean_venue_name,clean_date_posted,clean_country,clean_date_added,clean_instagram_user_id,clean_instagram_user_followers,clean_instagram_user_link,clean_instagram_media_id,clean_instagram_image_text,clean_instagram_comment_count,clean_instagram_like_count,clean_instagram_direct_image_link,clean_instagram_image_description,clean_instagram_handle,clean_instagram_image_link,terms_brand,terms_term,brpmen_posts_unique_id,source)
##                        cnxn.commit()
##                        num_of_new_posts = num_of_new_posts + 1
##                        print "inserted new instagram post!"
                               
                    if str(clean_instagram_media_id) in str(list_dc):
                        pass
                        #print "we already have this instagram post!"
                if date_posted_unix < time_then:
                    pass

### TIMER STOPS
stop = timeit.default_timer()
run_time = stop - start
m, s = divmod(run_time, 60)
h, m = divmod(m, 60)
hms_run_time = "%dh %02dm %02ds" % (h, m, s)

total_num_of_posts = num_of_posts_before_running_script + num_of_new_posts
str_total_num_of_posts = str(total_num_of_posts)
str_num_of_new_posts = str(num_of_new_posts)

str_time_end = str(datetime.datetime.now())

### TOP LINE DETAILS ARE LOGGED HERE

with open('cleaner_log.txt', 'w') as success_message:
    success_message.write("Script finished successfully!" + "\n")
    success_message.write("Script started at " + str_logging_time + "\n")
    success_message.write("Script stopped at " + str_time_end + "\n")
    success_message.write("This script took " + hms_run_time + " to run" + "\n")
    success_message.write("The number of posts on the system before the script ran was " + str_num_of_posts_before_running_script + "\n")
    success_message.write("The number of posts on the system after the script has ran is " + str_total_num_of_posts + "\n")
    success_message.write(str_num_of_new_posts + " new posts were added")
    print "Script finished. Refer to facebook_log.txt for top line stats"
success_message.close()

scope = ['https://spreadsheets.google.com/feeds']
wks.update_acell('A47', 'Script finished!')
wks.update_acell('B48', str_logging_time)
wks.update_acell('B49', str_time_end)
wks.update_acell('B50', hms_run_time)
wks.update_acell('B51', str_num_of_posts_before_running_script)
wks.update_acell('B52', str_total_num_of_posts)
wks.update_acell('B53', str_num_of_new_posts)




                

