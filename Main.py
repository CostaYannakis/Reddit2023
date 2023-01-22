import praw
import csv
from datetime import datetime
from datetime import timedelta
import yfinance as yf
import time
import requests
import json
import MyRedditFunctions
url = "https://www.reddit.com/r/ASX_Bets/comments/mah9je/premarket_thread_for_general_trading_and_plans/"
time10am = 10 * 60 *60
timelocalfromUTC = 11 * 60 * 60
today=datetime.today().strftime('%Y-%m-%d')
lasttwo=(datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')
yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
thread = dict()
counter = 0
redtitle = []
redscore = []
Asxcode = []
AsxCompanyName =[]
Time = []
AsxcodeCount = dict()
timeIntervals=20

hitDate = []
hitUrl = []
hitAsxCode = []
hitUpvotes = []
hitNumberComments = []
hitTitle = []


revisedDate= []
revisedUrl = []
revisedAsxCode = []
revisedUpvotes = []
revisedTitle =[]

Stocks = []
threadStocks = []

dailydiscussionstocks = []


#create an empty dictionary, this holds total stock mentions per day for the post
dictAsxCodeMentions = {}



######
DailyDate = []
DailyUrl = []

######
## we are concatinating two attributes to create a unique key for the DB Table to
##  avoid entering duplicated entries
def concatForUniqueIdentifier(created,thename):
    UniqueIdentifier = str(created)+str(thename)
    return UniqueIdentifier

reddit = praw.Reddit(
     client_id="VEICFOAA4ExqXw",
     client_secret="ss8VRW63QwTe30YpBK0PlE8DcbsPlw",
     user_agent="flannakis"
 )
print(reddit.read_only)

### ASX stock tickers in the csv below

## AUS
with open('companies-list.csv', 'r') as file:
## US 
## with open('USTickers.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        Asxcode.append(row[0])
        AsxCompanyName.append(row[1])
        dictAsxCodeMentions[row[0]]=0

####  Step One: We append the csv data to two Lists to contain the URLs and Date
with open('reddit2023\99daily.csv', 'r', encoding='utf-8-sig') as file:
    reader = csv.reader(file)
    for row in reader:
        DailyDate.append(row[0])
        DailyUrl.append(row[1])

print(DailyUrl)
####  Step Two: Add the .json to the url name
for i in range(len(DailyUrl)):
    DailyUrl[i] = DailyUrl[i] + ".json"

#### send to console to test output
print(DailyUrl)
print(DailyDate)

#### Test the first item in the list for the text out put
response = requests.get(DailyUrl[0], headers = {'User-agent': 'your bot 0.1'})
print(type(response))
##(playing around with json)

jsonified = response.json()
print(type(jsonified))

## output of jsonified is a list with two values [0] or [1]
## [1] holds the date we need and it is of type dict, lets dig deeper
## jsonified[1].keys() will yield `dict_keys(['kind', 'data'])`
## the date we need is in, well... data
## to call the data we use jsonified[1]['data']
## type(jsonified[1]['data']) is a dict again
## jsonified[1]['data'].keys() yields dict_keys(['after', 'dist', 'modhash', 'geo_filter', 'children', 'before'])
## all the details we need reside in children key
## type(jsonified[1]['data']['children']) now we are working with a list
## len(jsonified[1]['data']['children']) will yield the number of parent comments

Numberofcomments = len(jsonified[1]['data']['children'])
## working with a list means we can iterare throught it
## type(jsonified[1]['data']['children'][0]) yields another dict
## jsonified[1]['data']['children'][0].keys() yields dict_keys(['kind', 'data'])
## type(jsonified[1]['data']['children'][0]['data']) yields a dict

## jsonified[1]['data']['children'][0]['data'].keys() yields
## dict_keys(['subreddit_id', 'approved_at_utc', 'author_is_blocked',
## 'comment_type', 'awarders', 'mod_reason_by', 'banned_by', 'author_flair_type'
##, 'total_awards_received', 'subreddit', 'author_flair_template_id', 'likes',
##'replies', 'user_reports', 'saved', 'id', 'banned_at_utc', 'mod_reason_title',
## 'gilded', 'archived', 'collapsed_reason_code', 'no_follow', 'author',
## 'can_mod_post', 'created_utc', 'send_replies', 'parent_id', 'score',
## 'author_fullname', 'approved_by', 'mod_note', 'all_awardings', 'collapsed',
## 'body', 'edited', 'top_awarded_type', 'author_flair_css_class', 'name',
##'is_submitter', 'downs', 'author_flair_richtext', 'author_patreon_flair',
## 'body_html', 'removal_reason', 'collapsed_reason', 'distinguished',
## 'associated_award', 'stickied', 'author_premium', 'can_gild',
## 'gildings', 'unrepliable_reason', 'author_flair_text_color',
## 'score_hidden', 'permalink', 'subreddit_type', 'locked', 'report_reasons',
## 'created', 'author_flair_text', 'treatment_tags', 'link_id',
## 'subreddit_name_prefixed', 'controversiality', 'depth',
## 'author_flair_background_color', 'collapsed_because_crowd_control',
##'mod_reports', 'num_reports', 'ups'])

## but we are only interest in the following keys; 
##  "awarders","replies","author","created_utc","parent_id","score","author_fullname",
## "body","name","created"

## We only want to place these in a DB when there is a positive hit on a Stock ticker

## Lets create an array for the keys we want to extract

## maybe this should be stored in another python file?
cars = ["awarders","replies","author","created_utc","parent_id","score","author_fullname","body","name","created"]

## Lets also create a python array for stock tickers
## -1 below is for the last dict not having a body key)
for i in range(Numberofcomments -1):
    tickerCountPerPost = 0 
    for tickercode in Asxcode:
       if tickercode in jsonified[1]['data']['children'][i]['data']['body']:
           print(str(i)) 
           print(tickercode)
           tickerCountPerPost += 1
           dictAsxCodeMentions[tickercode]+=1 


    if tickerCountPerPost == 1:
        print("Do Something with" + str(i))
        print(jsonified[1]['data']['children'][i]['data']['created_utc'])
        print(jsonified[1]['data']['children'][i]['data']['body'])
        UID = concatForUniqueIdentifier(jsonified[1]['data']['children'][i]['data']['created_utc'],jsonified[1]['data']['children'][i]['data']['author'])
        print(UID)  
    else:
        print("Discard comment" + str(i))
    print("The Ticker count for comment " + str(i)+  " is: "  + str(tickerCountPerPost))
       

   #print(str(i)) 
   #print (jsonified[1]['data']['children'][i]['data']['body'])
