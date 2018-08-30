import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

# Here we have to describe what specifically we want to store
class Place(scrapy.Item):
    base_coordinates = scrapy.Field()
    coordinates = scrapy.Field()
    name = scrapy.Field()
    rating = scrapy.Field()
    price_level = scrapy.Field()
    types = scrapy.Field()
    formatted_address = scrapy.Field()
    place_id = scrapy.Field()
    photos = scrapy.Field()


class PlaceLoader(ItemLoader):

    default_output_processor = TakeFirst()

