
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
        soup = BeautifulSoup(markup)
        events = soup.find_all("div", class_="event")
        if events:
            for row in events:
                cols = row.find_all('div')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])
            print('Found {0} events for {1}'.format(len(data), symbol))
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
            print('successfully added to event-book')
        except:
            print('unable to add to event-book')

        if 'Date' in self.book.columns:
            self.book.Date = pd.to_datetime(self.book.Date)
            self.book = self.book.sort('Date')
