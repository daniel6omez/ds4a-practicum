# -*- coding: utf-8 -*-
#6.178602199999999,-75.65570925
#@6.1958298,-75.5858523,17z
#6.1958298,-75.5858523,
#re.findall("window.APP_INITIALIZATION_STATE=(.+?);\n", response.body.decode("utf-8"), re.S)

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GoogleMapsItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    pass

class PostalCodeItem(scrapy.Item):
    # define the fields for your item here like:
    postalCode = scrapy.Field()
    state = scrapy.Field()
    city = scrapy.Field()
    locType = scrapy.Field()
    boroughs = scrapy.Field()
    otherBoroughs = scrapy.Field()
    pass