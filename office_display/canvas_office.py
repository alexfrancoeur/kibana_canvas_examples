#!/usr/bin/python
import json
import elasticsearch
import pprint
import time
import random
from datetime import datetime, date, time, timedelta
import pytz
from newsapi import NewsApiClient
import pyowm
from yahoo_fin import stock_info as si

# VARIABLES
place = 'Newburyport,US'
ticker = 'ESTC'
local_domains = 'bostonglobe.com,bostonherald.com'
tech_domains = 'techcrunch,wired,the-verge,hacker-news'
country = 'us'

host = ["localhost"]
port = 9200
username = "elastic"
password = "changme"

index_name = "office_display_{0}".format((datetime.now()).strftime("%Y-%m-%d"))
elastic_query = '"elastic stack" OR elasticsearch OR kibana'
language = 'en'
own_key = 'Get key from https://openweathermap.org/api'
news_key = 'Get key from https://newsapi.org/'


##### MAPPINGS ######
mapping = {
    "settings": {
        "max_docvalue_fields_search": 200,
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
}

##### CREATE INDEX ######
try:
    es = elasticsearch.Elasticsearch(host,port=port,http_auth=(username,password))
except Exception as e:
    print(e)
    pprint.pprint("--------------")
try:
    es.indices.create(index=index_name,body=mapping, ignore=400)
except Exception as e:
    print(e)
    pprint.pprint("--------------")

####### HELPER FUNCTIONS #######

def reset():
    forecast_day["temp_min"] = 999
    forecast_day["temp_max"] = -999
    forecast_day["weather_code"] = 999
    forecast_day["status"] = 'something'

def article_helper(articles):
    articles_json = json.loads(json.dumps(articles["articles"]))
    article_count = 0
    list = []
    for a in articles_json:
        if article_count < 5:
            if (a["description"] is not None and a["title"] is not None and a["urlToImage"] is not None):
                list.append(a)
                article_count += 1
        else:
            return list

####### NEWS #######
# Init
newsapi = NewsApiClient(api_key=news_key)

# top global headlines
top_headlines = article_helper(newsapi.get_top_headlines(country=country))
top_5_global_headlines = {
    "article_01": top_headlines[0],
    "article_02": top_headlines[1],
    "article_03": top_headlines[2],
    "article_04": top_headlines[3],
    "article_05": top_headlines[4]
}

# top tech headlines
tech_headlines = article_helper(newsapi.get_top_headlines(sources=tech_domains))
top_5_tech_headlines = {
    "article_01": tech_headlines[0],
    "article_02": tech_headlines[1],
    "article_03": tech_headlines[2],
    "article_04": tech_headlines[3],
    "article_05": tech_headlines[4]
}

# local headlines
local_headlines = article_helper(newsapi.get_everything(domains=local_domains,sort_by='publishedAt'))
top_5_local_headlines = {
    "article_01": local_headlines[0],
    "article_02": local_headlines[1],
    "article_03": local_headlines[2],
    "article_04": local_headlines[3],
    "article_05": local_headlines[4]
}

# elastic stack headlines
elastic_headlines = article_helper(newsapi.get_everything(q=elastic_query,language=language,sort_by='publishedAt'))
top_5_elastic_headlines = {
    "article_01": elastic_headlines[0],
    "article_02": elastic_headlines[1],
    "article_03": elastic_headlines[2],
    "article_04": elastic_headlines[3],
    "article_05": elastic_headlines[4]
}

####### WEATHER #######
owm = pyowm.OWM(own_key)

# Current Weather
observation = owm.weather_at_place(place)
w = observation.get_weather()
l = observation.get_location()
weather_current = {
    "name": l.get_name(),
    #"location": "{0},{1}".format(l.get_lat(),l.get_lon()),
    "reception_time": observation.get_reception_time(timeformat='iso').replace(' ','T'),
    "wind": w.get_wind(unit="miles_hour"),
    "rain": w.get_rain(),
    "snow": w.get_snow(),
    "humidity": w.get_humidity(),
    "temperature": w.get_temperature('fahrenheit'),
    "status": w.get_status(),
    "weather_code": w.get_weather_code(),
    "detailed_status": w.get_detailed_status(),
    "sunset_time": w.get_sunset_time('iso').replace(' ','T'),
    "sunrise_time": w.get_sunrise_time('iso').replace(' ','T')
}

# Weather Forecast
fc = owm.three_hours_forecast(place)
f = fc.get_forecast()
lst = f.get_weathers()

forecast_day = {}
reset()
forecasts = []
forecast_day["date"] = (datetime.now()+ timedelta(hours=4)).strftime("%Y-%m-%d")
for x in lst:
    ref_date = datetime.strptime(x.get_reference_time('iso'),"%Y-%m-%d %H:%M:%S+00")+ timedelta(hours=4)
    if (ref_date.strftime("%Y-%m-%d")==forecast_day["date"]) :
        x_data = json.loads(x.to_JSON())
        if (x.get_temperature('fahrenheit')['temp_min']<forecast_day["temp_min"]) :
            forecast_day["temp_min"] = x.get_temperature('fahrenheit')['temp_min']
        if (x.get_temperature('fahrenheit')['temp_max']>forecast_day["temp_max"]) :
            forecast_day["temp_max"]=  x.get_temperature('fahrenheit')['temp_max']
        if (x.get_weather_code() < forecast_day["weather_code"]) :
            forecast_day["weather_code"] = x.get_weather_code()
            forecast_day["status"] = x.get_status()
    elif ref_date > datetime.strptime(forecast_day["date"],"%Y-%m-%d"):
        #persist day
        forecasts.append(forecast_day)
        # reset
        forecast_day = {}
        reset()
        ref_date = datetime.strptime(x.get_reference_time('iso'),"%Y-%m-%d %H:%M:%S+00")+ timedelta(hours=4)
        forecast_day["date"] = ref_date.strftime("%Y-%m-%d")
        if (ref_date.strftime("%Y-%m-%d")==forecast_day["date"]) :
            x_data = json.loads(x.to_JSON())
            if (x.get_temperature('fahrenheit')['temp_min']<forecast_day["temp_min"]) :
                forecast_day["temp_min"] = x.get_temperature('fahrenheit')['temp_min']
            if (x.get_temperature('fahrenheit')['temp_max']>forecast_day["temp_max"]) :
                forecast_day["temp_max"]=  x.get_temperature('fahrenheit')['temp_max']
            if (x.get_weather_code() < forecast_day["weather_code"]) :
                forecast_day["weather_code"] = x.get_weather_code()
                forecast_day["status"] = x.get_status()

weather_forecast = {
    "day_01": forecasts[0],
    "day_02": forecasts[1],
    "day_03": forecasts[2],
    "day_04": forecasts[3],
    "day_05": forecasts[4]
}

stock_price = si.get_live_price(ticker)
qt = si.get_quote_table(ticker)
stock_close = qt['Previous Close']
stock_open = qt['Open']
stock_day_range = qt["Day's Range"]
stock_52_range = qt["52 Week Range"]
stock_estimate = qt["1y Target Est"]
stock_volume = qt['Volume']
stock_mkt_cap = qt['Market Cap']


##### DOCUMENT ######

body = {
    "@timestamp": (datetime.now() + timedelta(hours=4)).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
    "headlines_global": top_5_global_headlines,
    "headlines_tech": top_5_tech_headlines,
    "headlines_local": top_5_local_headlines,
    "headlines_elastic": top_5_elastic_headlines,
    "weather_current": weather_current,
    "weather_forecast": weather_forecast,
    "stock_price": stock_price,
    "stock_close": stock_close,
    "stock_open": stock_open,
    "stock_day_range": stock_day_range,
    "stock_52_range": stock_52_range,
    "stock_estimate": stock_estimate,
    "stock_volume": stock_volume,
    "stock_mkt_cap": stock_mkt_cap
}

try:
    res = es.index(index=index_name, doc_type="_doc", body=body)
    pprint.pprint(res['result'])
    pprint.pprint("--------------")
except Exception as e:
    print(e)
    pprint.pprint("--------------")
