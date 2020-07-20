# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import geopandas as gpd
import numpy as np
from google_maps.items import PostalCodeItem

class PostalCodesSpiderSpider(scrapy.Spider):
    name = 'postal_codes_spider'

    def start_requests(self):
        url_postal_codes = "https://ds4a.blob.core.windows.net/ds4a/MedPostalCode.geojson"
        pc_df = gpd.read_file(url_postal_codes)
        for i, item in pc_df[['codigo_pos']].iterrows():
            url = 'https://col.youbianku.com/es/postcode/'+item.codigo_pos
            yield scrapy.Request(url,callback = self.parse)  

    def parse(self, response):
        pattern = r'(\w+)'
        item = PostalCodeItem()
        item['postalCode'] = response.css("li:contains('Código Postal') span::text").re_first(r'(\d+)') 
        item['state'] = response.css("li:contains('Provincia') a::text").extract_first()
        item['city'] = response.css("li:contains('Ciudad') a::text").extract_first()
        item['locType'] = response.css("li:contains('TIPO')::text").re_first(pattern) 
        item['boroughs'] = response.css("li:contains('BARRIOS CONTENIDOS EN EL CODIGO POSTAL')::text").extract_first().replace(': ','')
        item['otherBoroughs'] = response.css("li:contains('VEREDAS CONTENIDAS EN EL CODIGO POSTAL')::text").extract_first().replace(': ','')
        yield item
