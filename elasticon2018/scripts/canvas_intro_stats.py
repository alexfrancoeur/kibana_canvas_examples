#!/usr/bin/python
import elasticsearch
import pprint
import time
import datetime
import random
import pytz

es = elasticsearch.Elasticsearch(['localhost'],port=9400,http_auth=("elastic","Elastic2018!"))
#es = elasticsearch.Elasticsearch(['localhost'],port=9200)

mapping = {
    "mappings" : {
            "canvas_stats" : {
                "properties" : {
                        "timestamp" : { "type" : "date" },
                        "total_downloads" : { "type" : "long" },
                        "unique_users" : { "type" : "long" },
                        "reports_generated" : { "type" : "long" },
                        "office_displays" : { "type" : "long" },
                        "custom_plugins" : { "type" : "long" },
                        "mini_apps" : { "type" : "long" },
                        "status" : {"type":"keyword"},
                        "url" : {"type":"keyword"},
                        "os" : {"type":"keyword"},
                        "country" : {"type":"keyword"},
                }
            }
    }
}

pprint.pprint(mapping)

es.indices.create(index="canvas_stats",body=mapping, ignore=400)

# first doc
total_downloads = 1199999
unique_users = 749900
reports_generated = 2499000
office_displays = 500
custom_plugins = 100
mini_apps = 250
status = "good"
url = "http://canvas.elastic.co/"
os = "osx"
country = "US"

# lists
status_list = ["good", "warning", "severe"]
url_list = ["http://canvas.elastic.co/","http://canvas.elastic.co/stories/installing.html", "http://canvas.elastic.co/videos/index.html", "http://canvas.elastic.co/index.html/stories/index.html","http://canvas.elastic.co/blog/00029-more-example-workpads.html", "http://canvas.elastic.cox/reference/index.html", "http://canvas.elastic.co/reference/functions.html", "http://canvas.elastic.co/videos/101-welcome1.html", "http://canvas.elastic.co/blog/00028-canvas-and-coffee.html"]
os_list = ["ios","osx","win xp", "win 8", "win 7"]
country_list = ["US","CN","CA","FR","BR","DE","JP","AU"]

while True:
    try:
        canvas_doc = {}
        canvas_doc['timestamp'] = str(pytz.utc.localize(datetime.datetime.utcnow())).replace(' ','T')
        print(canvas_doc['timestamp'])
        canvas_doc['total_downloads'] = total_downloads
        canvas_doc['unique_users'] = unique_users
        canvas_doc['reports_generated'] = reports_generated
        canvas_doc['office_displays'] =  office_displays
        canvas_doc['custom_plugins'] = custom_plugins
        canvas_doc['mini_apps'] = mini_apps
        canvas_doc['status'] = status
        canvas_doc['url'] = url
        canvas_doc['os'] = os
        canvas_doc['country'] = country

        es.index(index="canvas_stats", doc_type="canvas_stats", id=canvas_doc['timestamp'], body=canvas_doc)
        pprint.pprint(canvas_doc)

        total_downloads += random.randint(0,10000)
        unique_users += random.randint(0,5000)
        reports_generated += random.randint(0,10000)
        office_displays += random.randint(0,1000)
        custom_plugins += random.randint(0,500)
        mini_apps += random.randint(0,50)
        status = random.choice(status_list)
        url = random.choice(url_list)
        os = random.choice(os_list)
        country = random.choice(country_list)

        if unique_users > 2350000:
            total_downloads = 1199999
            unique_users = 749900
            reports_generated = 2499000
            office_displays = 500
            custom_plugins = 100
            mini_apps = 250
            status = "good"
            url = "http://canvas.elastic.co/"
            os = "osx"
            country = "US"
    except:
        print "Error contacting elasticsearch"
    print "sleeping for 5 sec"
    time.sleep(5)
