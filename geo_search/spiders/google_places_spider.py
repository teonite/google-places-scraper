import scrapy
from geo_search.items import Place
from geo_search.items import PlaceLoader
import json


class GooglePlacesSpider(scrapy.Spider):
    name = 'GooglePlacesSpider'

    # Take attributes required to specify parameters used to prepare Spider
    def __init__(self, cords=None, radius=None, api_key=None, *args, **kwargs):
        super(GooglePlacesSpider, self).__init__(*args, **kwargs)

        # Store coordinates in the property. It will be useful in the database
        self.cords_dict = {
            "latitude": cords.split(',')[0],
            "longitude": cords.split(',')[1]
        }
        self.radius = radius

        # List which specify which data we want to request to the API
        fields = ['price_level', 'rating', 'types', 'name', 'formatted_address', 'geometry', 'place_id', 'photos']

        # create a query for API
        self.query = f'inputtype=textquery&input=*&locationbias=circle:{self.radius}@{cords}'
        self.query = f'{self.query}&fields={",".join(fields)}&key={api_key}'

        self.start_urls = [f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?{self.query}']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """ This function parses JSON data from the API and sends it to the pipeline

        @url https://maps.googleapis.com/maps/api/place/findplacefromtext/json?inputtype=textquery&input=*&locationbias=circle:200@53.4504331,14.5340195&fields=price_level,rating,types,name,formatted_address,geometry,place_id,photos&key=AIzaSyCIm9jIl-zaP4H6l3idynOMHxiE4rQEyi0
        @returns requests 0 0
        @scrapes base_coordinates coordinates name types formatted_address place_id types
        """

        # Parse json data into dictionary
        returned_data = json.loads(response.body)
        # Check if response status is ok
        if returned_data['status'] == 'OK':
            # Populate items using places data
            for place in returned_data['candidates']:

                loader = PlaceLoader(item=Place(), response=response)
                loader.add_value('base_coordinates', self.cords_dict)

                if 'geometry' in place:
                    loader.add_value('coordinates', place['geometry']['location'])
                if 'types' in place:
                    loader.add_value('name', place['name'])
                if 'types' in place:
                    loader.add_value('types', place['types'])
                if 'formatted_address' in place:
                    loader.add_value('formatted_address', place['formatted_address'])
                if 'place_id' in place:
                    loader.add_value('place_id', place['place_id'])
                if 'rating' in place:
                    loader.add_value('rating', place['rating'])
                if 'price_level' in place:
                    loader.add_value('price_level', place['price_level'])
                if 'photos' in place:
                    loader.add_value('photos', place['photos'])
                yield loader.load_item()
        else:
            print(returned_data['status'])
            self.log("Coś nie tak z requestem")
