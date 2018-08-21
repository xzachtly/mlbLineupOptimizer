#This web site lists recent injuries for MLB players in HTML format, but requires you to click each team, etc. 
#http://mlb.mlb.com/mlb/fantasy/injuries/
#To do real data analysis, we want a shitton and don't have time to click everywhere.
#So our exercise is to get all available injuries into one easy to use spreadsheet.

#By looking at "view source" on the web site, I found that the web site actually hits another web site, which provides the injuries, trades and other info in a computer-readable format called JSON, which is basically
#the same as python's dictionary type. You can only get one month at a time bc there are so many. See it here:
#http://mlb.mlb.com/lookup/json/named.transaction_all.bam?start_date=20120301&end_date=20120401&sport_code='mlb'
#Our code will hit this web site repeatedly for different dates, convert the web site's content into a python object, and then write certain fields from that object to a file of the CSV format




#import these standard python modules so we can call certain functions. you just google them to know what kind of modules are provided and how to use them, basically
from urllib.request import urlopen
import json
import calendar
import csv


#a CSV is a comma-separated text file to open in Excel--a spreadsheet that should have the following fields.
header = ['orig_asset_type', 'player', 'team_id', 'trans_date_cd', 'player_id', 'conditional_sw', 'name_sort', 'note', 'type_cd', 'trans_date', 'from_team', 'effective_date', 'type', 'transaction_id', 'orig_asset', 'final_asset_type', 'from_team_id', 'final_asset', 'resolution_cd', 'resolution_date', 'name_display_last_first', 'name_display_first_last', 'team']
#create and open a text file and allow us to write to it
fout = csv.DictWriter( open('masterjp.csv','w'), header)
fout.writeheader()

def scrapetocsv():
    #our getmonth() function is the meat of the work; this just loops thru and calls it repeatedly on different years and months
    for year in range(2017,2018):
        for month in range(1,13):
            getmonth(year,month)
            
    for month in range(1,5):
        getmonth(2012,month)        



def getmonth(year,month):

    print(year, month)

    maxday = calendar.monthrange(year,month)[1]
    monthstr = str(month) #convert number type to string type and make it two digits if it's less than 10 (october) to format YYYMMDD
    if len(monthstr)<2: #len() returns either the number of items in a list or the number of characters in a string
        monthstr = '0' + monthstr
    start = '%s%s01' % (year,monthstr)
    end = '%s%s%02d' % (year,monthstr,maxday)
    url = "http://mlb.mlb.com/lookup/json/named.transaction_all.bam?start_date=%s&end_date=%s&sport_code='mlb'" % (start,end)
    
    #this opens a web site and saves its HTML code
    response = urlopen(url).read()
    data = json.loads(response)['transaction_all']['queryResults']

    if 'row' in data.keys():
        if type(data['row']) is dict:
            #only one transaction
            rows = [ data['row'], ]
        else:
            rows = data['row']
        for row in rows:
            #there are trades in here, but we only want injuries. "'x' in var" can simply test whether a substring is within a certain string
            descrip = row['note'].lower() #use lowercase text
            #if you get rid of this 'if' condition your spreadsheet will also have trades and shit to explore
            if 'disabled' in descrip or 'DL' in descrip or 'injur' in descrip:
                fout.writerow(row)

#this other stuff is indented functions so it doesn't run. This final line is not indented, so it is the actuall trigger that is pulled to call the functions and do everything            
scrapetocsv()

#Now open up your spreadsheet (masterjp.csv). Left to you: look up and download SQLlite, the easiest-to-install version of the SQL database, and figure out how to import the spreadsheet
#into a database table and answer some questions: 
#Which team had the most injuries?
#SELECT team, count(*) from mlb GROUP BY team ORDER BY count(*) desc;
#Which Yankee had the most injuries?
#SELECT player, count(*) from mlb WHERE team LIKE '*YANKEES*' GROUP BY player ORDER BY count(*) desc;

