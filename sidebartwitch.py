#sidebar twitch updater
#made by /u/s8l
#March 15, 2015

#make sure to "sudo pip install praw"
#if you are on windows you will need to install curl and edit the curl_location variable
import praw
from time import sleep 
import os
import subprocess
import HTMLParser
import json
import sys
####################################
handle="twitch status sidebar updater by /u/s8l Ver1"
curl_location="curl"#on windows it is likely "C://curl" if you follow http://curl.haxx.se/download.html and extract to c://
title=">**Twitch streams status**"
####################################


def help():
	print """
###################################
Twitch SideBar Updater ver 1 by /u/s8l
###################################
Usage:
sidebartwitch username password sub delay_in_sec twitch_stream1 [twitch_stream2 twitch_stream3 ....]"""
	return



def isStreaming(user):
	global curl_location
	command=curl_location+" -s -H 'Accept: application/vnd.twitchtv.v2+json' -X GET https://api.twitch.tv/kraken/streams/"+user+" -k"
	proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	stream=json.loads(out.decode())
		
	try:
		return (True if stream['stream'] else False)
	except:
		return False
	else:
		return False

def f_last(S,text,last_match=-1):
	x=S.find(text,last_match+1)
	if x==-1:
		return last_match
	return f_last(S,text,x)
		

########MAIN#########
if len(sys.argv)<6:
	help()
else:
	stream_users=len(sys.argv)-4
	user=sys.argv[1]
	passw=sys.argv[2]
	sub=sys.argv[3]
	delay=int(sys.argv[4])
	os.system( 'cls' if os.name == 'nt' else 'clear')
	print "Logging in. Check for praw.errors, otherwise the password is correct"
	r = praw.Reddit(handle)
	r.login(user,passw)	
	print "USER=",user
	print "SUB=",sub
	r.clear_authentication()
	print "Logged in"
	while(1):
		print "Updating",
		#login
		r = praw.Reddit(handle)
		r.login(user,passw)
		settings = r.get_settings(sub)	
		#parse html
		print ".",#login error
		htmldescription=settings['description']
		htmlparser=HTMLParser.HTMLParser()
		sidebar_contents = htmlparser.unescape(htmldescription)
		#delete old settings
		last=f_last(sidebar_contents, title)
		print ".",#parsing error
		if last>=0:
			sidebar_contents=sidebar_contents[0:last]
		else:
			sidebar_contents+="  \n"
		sidebar_contents+=title
		#add new streams
		for everystream in sys.argv[5:]:
			print everystream,
			sidebar_contents+="   \n>"+everystream+" "
			sidebar_contents+=("ON" if isStreaming(everystream) else "OFF")
		print ".",#twitch error
		#update status bar
		r.update_settings(r.get_subreddit(sub), description=sidebar_contents)
		print ".",#updating sidebar error
		r.clear_authentication()
		#wait
		print "Done"
		print "Next update in "+str(delay)+" seconds."
		sleep(delay)
		
		
		

	
	
