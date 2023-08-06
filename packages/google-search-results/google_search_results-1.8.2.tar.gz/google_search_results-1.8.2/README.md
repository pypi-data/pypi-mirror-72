# Google Search Results in Python

[![PyPI version](https://badge.fury.io/py/google-search-results.svg)](https://badge.fury.io/py/google-search-results)
[![Build Status](https://travis-ci.org/serpapi/google-search-results-python.svg?branch=master)](https://travis-ci.org/serpapi/google-search-results-python)

This Python package is meant to scrape and parse Google, Google Scholar, Bing, Baidu, Yandex, Yahoo, Ebay results using [SerpApi](https://serpapi.com). 

The following services are provided:
- [Search API](https://serpapi.com/search-api)
- [Search Archive API](https://serpapi.com/search-archive-api)
- [Account API](https://serpapi.com/account-api)
- [Location API](https://serpapi.com/locations-api) (Google Only)

SerpApi provides a [script builder](https://serpapi.com/demo) to get you started quickly.

## Installation

Python 3.7+
```bash
pip install google-search-results
```

[Link to the python package page](https://pypi.org/project/google-search-results/)

## Quick start

```python
from serpapi.google_search_results import GoogleSearchResults
client = GoogleSearchResults({"q": "coffee", "location": "Austin,Texas"})
result = client.get_dict()
```

This example runs a search about "coffee" using your secret api key.

The SerpApi service (backend)
- searches on Google using the client: q = "coffee"
- parses the messy HTML responses
- return a standardizes JSON response
The GoogleSearchResults class
- Format the request
- Execute GET http request against SerpApi service
- Parse JSON response into a dictionary
Et voila..

Alternatively, you can search:
- Bing using BingSearchResults class
- Baidu using BaiduSearchResults class
- Yahoo using YahooSearchResults class
- Ebay using EbaySearchResults class
- Yandex using YandexSearchResults class
- GoogleScholar using GoogleScholarSearchResults class

See the [playground to generate your code.](https://serpapi.com/playground)

## Summary
- [Google Search Results in Python](#google-search-results-in-python)
  - [Installation](#installation)
  - [Quick start](#quick-start)
  - [Summary](#summary)
    - [Google Search API capability](#google-search-api-capability)
    - [How to set SERP API key](#how-to-set-serp-api-key)
    - [Example by specification](#example-by-specification)
    - [Location API](#location-api)
    - [Search Archive API](#search-archive-api)
    - [Account API](#account-api)
    - [Search Bing](#search-bing)
    - [Search Baidu](#search-baidu)
    - [Search Yandex](#search-yandex)
    - [Search Yahoo](#search-yahoo)
    - [Search Ebay](#search-ebay)
    - [Search Google Scholar](#search-google-scholar)
    - [Generic search with SerpApiClient](#generic-search-with-serpapiclient)
    - [Search Google Images](#search-google-images)
    - [Search Google News](#search-google-news)
    - [Search Google Shopping](#search-google-shopping)
    - [Google Search By Location](#google-search-by-location)
    - [Batch Asynchronous Searches](#batch-asynchronous-searches)
  - [Change log](#change-log)
  - [Conclusion](#conclusion)

### Google Search API capability
Source code.
```python
params = {
  "q": "client",
  "google_domain": "Google Domain", 
  "location": "Location Requested", 
  "device": "desktop|mobile|tablet",
  "hl": "Google UI Language",
  "gl": "Google Country",
  "safe": "Safe Search Flag",
  "num": "Number of Results",
  "start": "Pagination Offset",
  "serp_api_key": "Your SERP API Key", 
  # To be match
  "tbm": "nws|isch|shop", 
  # To be search
  "tbs": "custom to be search criteria",
  # allow async request
  "async": "true|false",
  # output format
  "output": "json|html"
}

# define the search client
client = GoogleSearchResults(params)
# override an existing parameter
client.params_dict["location"] = "Portland"
# search format return as raw html
html_results = client.get_html()
# parse results
dict_results = client.get_dict()
json_results = client.get_json()
```
[Link to the full documentation](https://serpapi.com/search-api)

see below for more hands on examples.

### How to set SERP API key

You can get an API key here if you don't already have one: https://serpapi.com/users/sign_up

The SerpApi `api_key` can be set globally:
```python
GoogleSearchResults.SERP_API_KEY = "Your Private Key"
```
The SerpApi `api_key` can be provided for each client:
```python
query = GoogleSearchResults({"q": "coffee", "serp_api_key": "Your Private Key"})
```

### Example by specification

We love true open source, continuous integration and Test Drive Development (TDD). 
 We are using RSpec to test [our infrastructure around the clock](https://travis-ci.org/serpapi/google-search-results-python) to achieve the best QoS (Quality Of Service).
 
The directory test/ includes specification/examples.

Set your api key.
```bash
export API_KEY="your secret key"
```

Run test
```python
make test
```

### Location API

```python
from serpapi.google_search_results import GoogleSearchResults
client = GoogleSearchResults({})
location_list = client.get_location("Austin", 3)
print(location_list)
```

it prints the first 3 location matching Austin (Texas, Texas, Rochester)
```python
[   {   'canonical_name': 'Austin,TX,Texas,United States',
        'country_code': 'US',
        'google_id': 200635,
        'google_parent_id': 21176,
        'gps': [-97.7430608, 30.267153],
        'id': '585069bdee19ad271e9bc072',
        'keys': ['austin', 'tx', 'texas', 'united', 'states'],
        'name': 'Austin, TX',
        'reach': 5560000,
        'target_type': 'DMA Region'},
        ...]
```

### Search Archive API

The search result are stored in temporary cached.
The previous search can be retrieve from the the cache for free.

```python
from serp.google_search_results import GoogleSearchResults
client = GoogleSearchResults({"q": "Coffee", "location": "Austin,Texas"})
search_result = client.get_dictionary()
search_id = search_result.get("search_metadata").get("id")
print(search_id)
```

Now let retrieve the previous search from the archive.

```python
archived_search_result = GoogleSearchResults({}).get_search_archive(search_id, 'json')
print(archived_search_result.get("search_metadata").get("id"))
```
it prints the search result from the archive.

### Account API
```python
from serpapi.google_search_results import GoogleSearchResults
client = GoogleSearchResults({})
account = client.get_account()
```
it prints your account information.

### Search Bing
```python
from serpapi.bing_search_results import BingSearchResults
client = BingSearchResults({"q": "Coffee", "location": "Austin,Texas"})
data = client.get_json()
```
this code prints baidu search results for coffee as JSON. 

https://serpapi.com/bing-search-api

### Search Baidu
```python
from serpapi.baidu_search_results import BaiduSearchResults
client = BaiduSearchResults({"q": "Coffee"})
data = client.get_json()
```
this code prints baidu search results for coffee as JSON. 
https://serpapi.com/baidu-search-api

### Search Yandex
```python
from serpapi.yandex_search_results import YandexSearchResults
client = YandexSearchResults({"text": "Coffee"})
data = client.get_json()
```
this code prints yandex search results for coffee as JSON. 

https://serpapi.com/yandex-search-api

### Search Yahoo
```python
from serpapi.yahoo_search_results import YahooSearchResults
client = YahooSearchResults({"p": "Coffee"})
data = client.get_json()
```
this code prints yahoo search results for coffee as JSON. 

https://serpapi.com/yahoo-search-api


### Search Ebay
```python
from serpapi.ebay_search_results import EbaySearchResults
client = EbaySearchResults({"_nkw": "Coffee"})
data = client.get_json()
```
this code prints ebay search results for coffee as JSON. 

https://serpapi.com/ebay-search-api

### Search Google Scholar
```python
from serpapi.google_scholar_search_results import GoogleScholarSearchResults
client = GoogleScholarSearchResults({"q": "Coffee"})
data = client.get_json()
```
this code prints Google Scholar search results.

### Generic search with SerpApiClient
```python
from serpapi.serp_api_client import SerpApiClient
query = {"q": "Coffee", "location": "Austin,Texas", "engine": "google"}
client = SerpApiClient(query)
data = client.get_json()
```
This class enables to interact with any search engine supported by SerpApi.com 

### Search Google Images

```python
from serpapi.google_search_results import GoogleSearchResults
client = GoogleSearchResults({"q": "coffe", "tbm": "isch"})
for image_result in client.get_json()['images_results']:
    link = image_result["original"]
    try:
        print("link: " + link)
        # wget.download(link, '.')
    except:
        pass
```

this code prints all the images links, 
 and download image if you un-comment the line with wget (linux/osx tool to download image).

This tutorial covers more ground on this topic.
https://github.com/serpapi/showcase-serpapi-tensorflow-keras-image-training

### Search Google News

```python
from serpapi.google_search_results import GoogleSearchResults
client = GoogleSearchResults({
    "q": "coffe",   # search client
    "tbm": "nws",  # news
    "tbs": "qdr:d", # last 24h
    "num": 10
})
for offset in [0,1,2]:
    client.params_dict["start"] = offset * 10
    data = client.get_json()
    for news_result in data['news_results']:
        print(str(news_result['position'] + offset * 10) + " - " + news_result['title'])
```

this script prints the first 3 pages of the news title for the last 24h.

### Search Google Shopping

```python
from serpapi.google_search_results import GoogleSearchResults
client = GoogleSearchResults({
    "q": "coffe",   # search client
    "tbm": "shop",  # news
    "tbs": "p_ord:rv", # last 24h
    "num": 100
})
data = client.get_json()
for shopping_result in data['shopping_results']:
    print(shopping_result['position']) + " - " + shopping_result['title'])

```

this script prints all the shopping results order by review order.

### Google Search By Location

With SerpApi, we can build Google search from anywhere in the world.
This code is looking for the best coffee shop per city.

```python
from serpapi.google_search_results import GoogleSearchResults
for city in ["new york", "paris", "berlin"]:
  location = GoogleSearchResults({}).get_location(city, 1)[0]["canonical_name"]
  client = GoogleSearchResults({
      "q": "best coffee shop",   # search client
      "location": location,
      "num": 1,
      "start": 0
  })
  data = client.get_json()
  top_result = data["organic_results"][0]["title"]
```

### Batch Asynchronous Searches

We do offer two ways to boost your searches thanks to `async` parameter.
 - Blocking - async=false - it's more compute intensive because the client would need to hold many connections. (default) 
  - Non-blocking - async=true - it's way to go for large amount of query submitted by batch  (recommended)

```python
# Python 3.6+
#

# Operating system
import os

# regular expression library
import re

# safe queue (named Queue in python2)
from queue import Queue

# Time utility
import time

# SerpApi client
from serpapi.google_search_results import GoogleSearchResults

# store searches
search_queue = Queue()
        
# SerpApi client
client = GoogleSearchResults({
    "location": "Austin,Texas",
    "async": True
})

# loop through a list of companies
for company in ['amd','nvidia','intel']:
  print("execute async search: q = " + company)
  client.params_dict["q"] = company
  search = client.get_dict()
  print("add search to the queue where id: " + search['search_metadata']['id'])
  # add search to the search_queue
  search_queue.put(search)

print("wait until all search statuses are cached or success")

# Create regular client
client = GoogleSearchResults({"async": True})
while not search_queue.empty():
  search = search_queue.get()
  search_id = search['search_metadata']['id']

  # retrieve search from the archive - blocker
  print(search_id + ": get search from archive")
  search_archived =  client.get_search_archive(search_id)
  print(search_id + ": status = " + search_archived['search_metadata']['status'])
  
  # check status
  if re.search('Cached|Success', search_archived['search_metadata']['status']):
    print(search_id + ": search done with q = " + search_archived['search_parameters']['q'])
  else:
    # requeue search_queue
    print(search_id + ": requeue search")
    search_queue.put(search)
    
    # wait 1s
    time.sleep(1)

# self.assertIsNotNone(results["local_results"][0]["title"])
print('all searches completed')
```

This code shows how to run searches asynchronously.
The search parameters must have {async: True}. This indicates that the client shouldn't wait for the search to be completed.
The current thread that executes the search is now non-blocking which allows to execute thousand of searches in seconds. The SerpApi backend will do the processing work.
The actual search result is defer to a later call from the search archive using get_search_archive(search_id).
In this example the non-blocking searches are persisted in a queue: search_queue.
A loop through the search_queue allows to fetch individual search result.
This process can be easily multithreaded to allow a large number of concurrent search requests.
To keep thing simple, this example does only explore search result one at a time (single threaded).

[See example.](https://github.com/serpapi/google-search-results-python/blob/master/tests/test_example.py)

## Change log
2020-03-25 @ 1.8
 - add support for Yandex, Yahoo, Ebay
 - clean-up test
2019-11-10 @ 1.7.1
 - increase engine parameter priority over engine value set in the class
2019-09-12 @ 1.7
 - Change  namespace "from lib." instead: "from serpapi.google_search_results import GoogleSearchResults"
 - Support for Bing and Baidu
2019-06-25 @ 1.6
 - New search engine supported: Baidu and Bing

## Conclusion
SerpApi supports all the major search engines. Google has the more advance support with all the major services available: Images, News, Shopping and more..
To enable a type of search, the field tbm (to be matched) must be set to:

 * isch: Google Images API.
 * nws: Google News API.
 * shop: Google Shopping API.
 * any other Google service should work out of the box.
 * (no tbm parameter): regular Google client.

The field `tbs` allows to customize the search even more.

[The full documentation is available here.](https://serpapi.com/search-api)
