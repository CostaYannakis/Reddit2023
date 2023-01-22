import sqlite3
counter = 0
import yfinance as yf
import datetime
import time
from datetime import timedelta
# Takes the Date and adds 10 hrs to UTC to create the ASX Stock Start time
def StockCutOff(Date):
    import time
    import datetime
    from datetime import timedelta
    #10 hours X 60 minutes X 60 seconds = 10 hrs converted to secs
    StockStartTime = 10 * 60 * 60
    #Takes the string date and its format and
    utc = time.mktime(datetime.datetime.strptime(Date, "%Y-%m-%d").timetuple())
    utcCutoff = utc + StockStartTime
    #returns the float value
    return utcCutoff

def createListEntry(myCounter,theList, theName, theTime, theUpvotes, thePost):

    dict = {}
    dict["ID"] = myCounter
    dict["name"] = theName
    dict["Time"] = theTime
    dict["Upvotes"] = theUpvotes
    dict["Post"] = thePost

    theList.append(dict)

def USStockCutOff(Date):
        import time
        import datetime
        from datetime import timedelta
        # 10 hours X 60 minutes X 60 seconds = 10 hrs converted to secs
        StockStartTime = (14 + 9.5) * 60 * 60
        # Takes the string date and its format and
        utc = time.mktime(datetime.datetime.strptime(Date, "%Y-%m-%d").timetuple())
        utcCutoff = utc + StockStartTime
        # returns the float value
        return utcCutoff





def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def nextDay(thedate):
    import time
    from datetime import datetime
    from datetime import timedelta
    date_time_obj = datetime.strptime(thedate, '%Y-%m-%d')
    dayoftheweek = date_time_obj.weekday()

    if dayoftheweek == 0 or dayoftheweek == 1 or dayoftheweek == 2 or dayoftheweek == 3:

        date_time_obj = date_time_obj + timedelta(days=1)

    else:
        date_time_obj = date_time_obj + timedelta(days=3)

    return date_time_obj.strftime('%Y-%m-%d')

def priorDay(thedate):
    import time
    from datetime import datetime
    from datetime import timedelta
    date_time_obj = datetime.strptime(thedate, '%Y-%m-%d')
    dayoftheweek = date_time_obj.weekday()

    if dayoftheweek == 1 or dayoftheweek == 2 or dayoftheweek == 3 or dayoftheweek == 4:
        date_time_obj = date_time_obj + timedelta(days=-1)

    else:
        date_time_obj = date_time_obj + timedelta(days=-3)


    return date_time_obj.strftime('%Y-%m-%d')

def getStockData2(ticker,startdate):
  OpenClose = []
  theStock = yf.Ticker(ticker)

  start1 = datetime.datetime.strptime(startdate, '%Y-%m-%d')
  #print(type(start1))


  nextday = datetime.timedelta(days=1) + start1
  #print(nextday)
  stockhistory = theStock.history(start=start1, end=nextday)
  time.sleep(.5)

  #print(stockhistory)
  DataTop = stockhistory.head()
  for row in DataTop.index:
      print(row, end=" ")
      print("_____________________")
      if stockhistory.iloc[0]["Close"] is None:
        print("fail")
      else:
        print("_____________________")
        print("success")
  #print((type(stockhistory.iloc[0]["Close"])))
  print(type(stockhistory))
  if not stockhistory.iloc[0]["Close"] and stockhistory.iloc[0]["Open"]:
    OpenClose.append(0)
    OpenClose.append(0)
  else:
    close1day = float((stockhistory.iloc[0]["Close"]))
    # print(close1day)
    open1day = float((stockhistory.iloc[0]["Open"]))
    # print(open1day)
    OpenClose.append(open1day)
    OpenClose.append(close1day)
    OpenClose.append(startdate)
    OpenClose.append(ticker)


  return OpenClose


#next = nextDay("2021-10-01")
#prior = priorDay("2021-10-01")

#print(next)
#print(prior)


def breaker():
    print("_____________________________________________________________")

def getMusk(ticker,startdate,enddate,intervalinput):

    start1 = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    end1 = datetime.datetime.strptime(enddate, '%Y-%m-%d')
    theStock = yf.Ticker(ticker)
    stockhistory = theStock.history(start=start1, end=end1, interval=intervalinput )
    return stockhistory






