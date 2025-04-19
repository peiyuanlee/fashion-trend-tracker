from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)
keywords = ['balletcore', 'grunge', 'gorpcore', 'y2k', 'avant-garde']
pytrends.build_payload(keywords, cat=0, timeframe='today 3-m', geo='', gprop='')

df = pytrends.interest_over_time()
df = df.reset_index()
df.to_csv('data/trends.csv', index=False)