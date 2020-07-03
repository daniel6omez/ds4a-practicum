# -*- coding: utf-8 -*-
import scrapy
from google_maps.items import GoogleMapsItem
import re
import pandas as pd

class GoogleMapsSpiderSpider(scrapy.Spider):
    name = 'google_maps_spider'

    def start_requests(self):
        df = pd.read_csv('../../../samples/processed/accidents_cleanV2.csv')
        df = df[(df.cbml.isna())]
        print(df.shape)
        for i, item in df[['radicado','direccion']].iterrows():
            meta= {'address':item['direccion']}
            meta['id']=str(item['radicado'])
            url = 'https://www.google.com/maps/search/'+item['direccion']+',Antioquia'
            yield scrapy.Request(url,
            meta=meta,
            callback = self.parse)   

    def parse(self, response):
        txt = response.xpath("//script[contains(., 'APP_INITIALIZATION_STATE=')]/text()").extract_first()
        item = GoogleMapsItem()
        lon_lat_array = re.findall(",null,null,null,null,null,null,\[null,null,(-?[\d]*\.[\d]*),(-?[\d]*\.[\d]*)\]", txt)[0]
        item['id']=response.meta['id']
        item['address']=response.meta['address']
        item['longitude'] = lon_lat_array[0]
        item['latitude'] = lon_lat_array[1]
        yield item
