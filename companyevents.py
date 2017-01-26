
from urllib import request
from bs4 import BeautifulSoup
import pandas as pd


class EventBook:

    def __init__(self):
        self.book = pd.DataFrame()

    # main function
    def get_events(self, symbol, add_to_book=False):
        data = []
        url = "http://www.google.com/finance?&q={0}".format(symbol)
        req = request.Request(url)
        resp = request.urlopen(req)
        markup = resp.read()
        soup = BeautifulSoup(markup, "lxml")
        events = soup.find_all("div", class_="event")
        if events:
            for row in events:
                cols = row.find_all('div')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])
            #print('Found {0} events for {1}'.format(len(data), symbol))
        else:
            print('No events found for symbol: {0}'.format(symbol))
        df = pd.DataFrame(data, columns=['Date', 'Event'])
        df['Symbol'] = symbol
        if add_to_book:
            self.add_to_eb([df])
        return df

    # supporting function
    def add_to_eb(self, list_like):
        # support func for get_events
        list_like.append(self.book)
        try:
            self.book = pd.concat(list_like)
            #print('successfully added to event-book')
        except:
            print('unable to add to event-book')

        if 'Date' in self.book.columns:
            self.book.Date = pd.to_datetime(self.book.Date)
            self.book = self.book.sort_values('Date')


def djia_earnings_calendar(beg_date=''):
    # creates an eventbook for earnings releases of companies in the dow jones 30
    # use as template for looping through list of symbols, searching strings, and slicing by date
    # arg 'beg_date' takes yyyy-mm-dd, or i suppose anything else that pandas will index on
    
    dj = EventBook()
    
    djia_symbols = ['AAPL','AXP','BA','CAT','CSCO','CVX','DD','DIS','GE','GS','HD','IBM','INTC','JNJ',
                'JPM','KO','MCD','MMM','MRK','MSFT','NKE','PFE','PG','TRV','UNH','UTX','V','VZ','WMT','XOM']
    
    symbs_found = 0
    for symbol in djia_symbols:
        tst = dj.get_events(symbol, add_to_book=True)
        if len(tst) > 0:
            symbs_found = symbs_found + 1
    if len(djia_symbols) == symbs_found:
        print('events found for all symbs in djia_symbols')
    
    dj.book['Event'] = dj.book['Event'].str.upper()
    djia_earnings = dj.book[dj.book['Event'].str.contains('EARNINGS')]
    
    
    if beg_date:
        djia_earnings = djia_earnings[djia_earnings['Date'] > beg_date]
        
    return djia_earnings
