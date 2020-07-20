# -*- coding: utf-8 -*-
import scrapy
from google_maps.items import GoogleMapsItem
import re
import pandas as pd

class GoogleMapsSpiderSpider(scrapy.Spider):
    name = 'google_maps_spider'

    def start_requests(self):
        df = pd.read_excel('../../../samples/raw/data/Incidentes2014_2020.xlsx')
        df = df[(df.Cbml.isna())]
        print(df.shape)
        for i, item in df[['radicado','direccion']].iterrows():
            meta= {'address':item['direccion']}
            meta['id']=str(item['radicado'])
            url = 'https://www.google.com/maps/search/'+item['direccion']+',Antioquia'
            yield scrapy.Request(url,
            meta=meta,
            callback = self.parse)   

    def parse(self, response):
        javascript = ''.join(response.css("script::text").extract()) 
        vars = javascript.split(';')
        index = 0
        for i,var in enumerate(vars): 
            if 'window.APP_INITIALIZATION_STATE' in var: 
                index = 0
        var = vars[index]   



        # javascript = response.css("script:contains('window.APP_INITIALIZATION_STATE')::text").get()  
        #txt = response.xpath("//script[contains(., 'APP_INITIALIZATION_STATE=')]/text()").extract_first()
        item = GoogleMapsItem()
        lon_lat_array = re.findall(",null,null,null,null,null,null,\[null,null,(-?[\d]*\.[\d]*),(-?[\d]*\.[\d]*)\]", var)[0]
        item['id']=response.meta['id']
        item['address']=response.meta['address']
        item['longitude'] = lon_lat_array[0]
        item['latitude'] = lon_lat_array[1]
        yield item
