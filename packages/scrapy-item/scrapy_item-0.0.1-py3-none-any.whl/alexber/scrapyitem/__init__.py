# -*- coding: utf-8 -*-

import scrapy

class GeneralItem(scrapy.Item):
    # # define the fields for your item here like:
    # # name = scrapy.Field()
    # data = scrapy.Field()

    # see https://stackoverflow.com/a/31944506/1137529
    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key] = scrapy.Field()
        # self._values[key] = value
        super().__setitem__(key, value)
