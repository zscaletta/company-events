# company-events
small module for creating public company event and earnings calendars from google finance html tables


## usage


get events for a single company

```python
import companyevents as ce

eb = ce.Eventbook()
eb.get_events('XOM')
```

create book of events for multiple companies

```python
import companyevents as ce

eandp = ce.EventBook()
eandp.get_events('XOM', add_to_book=True)
eandp.get_events('COP', add_to_book=True)
eandp.get_events('MRO', add_to_book=True)
eandp.book
```

create a calendar of earnings dates for DJIA companies

```python

import companyevents as ce

ce.djia_earnings_calendar(beg_date='2017-01-20')
```
