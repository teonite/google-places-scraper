import unittest
from unittest.mock import patch
from geo_search.spiders.google_places_spider import GooglePlacesSpider
import json


class TestGooglePlacesSpider(unittest.TestCase):


    def test_running_spider_with_parameters(self):
        """Check that arguments passed into spider was transformed correctly"""

        cords = '53.429907,14.5501827'
        cords_list = cords.split(',')
        radius = 200
        spider = GooglePlacesSpider(cords=cords, radius=radius)

        self.assertEqual(spider.cords_dict, {"latitude": cords_list[0], "longitude": cords_list[1]})
        self.assertEqual(spider.radius, radius)

    def test_url_to_api(self):
        """Check that Url was prepared correctly"""

        cords = '53.429907,14.5501827'
        cords_list = cords.split(',')
        radius = 200
        spider = GooglePlacesSpider(cords=cords, radius=radius)

        self.assertIn(cords_list[0], spider.query)
        self.assertIn(cords_list[1], spider.query)
        self.assertIn(str(radius), spider.query)

    @patch('geo_search.spiders.google_places_spider.scrapy', spec=True)
    def test_request_to_api(self, mock_scrapy):
        """Check that start_requests method calls scrapy.Request method with url parameter and with callback"""

        cords = '53.429907,14.5501827'
        radius = 200
        spider = GooglePlacesSpider(cords=cords, radius=radius)
        # start_requests method returns generator
        next(spider.start_requests())

        mock_scrapy.Request.assert_called_with(url=spider.start_urls[0], callback=spider.parse)

    # TODO: Finish that test
    def test_response_from_api(self):
        """Check that parse method return Item object in a correct way"""

        class MockResponse():
            def __init__(self):
                self.url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?inputtype=textquery&input=*&locationbias=circle:200@53.4504331,14.5340195&fields=price_level,rating,types,name,formatted_address,geometry,place_id,photos&key=AIzaSyCIm9jIl-zaP4H6l3idynOMHxiE4rQEyi0'
                self.text = "jakis tekst"
                self.body = {
                   "candidates" : [
                      {
                         "formatted_address" : "140 George St, The Rocks NSW 2000, Australia",
                         "geometry": {
                            "location": {
                               "lat": -33.8599358,
                               "lng": 151.2090295
                            },
                            "viewport": {
                               "northeast" : {
                                  "lat": -33.85824767010727,
                                  "lng": 151.2102470798928
                               },
                               "southwest": {
                                  "lat": -33.86094732989272,
                                  "lng": 151.2075474201073
                               }
                            }
                         },
                         "name" : "Museum of Contemporary Art Australia",
                         "opening_hours": {
                            "open_now": False,
                            "weekday_text": []
                         },
                         "photos": [
                            {
                               "height" : 2268,
                               "html_attributions" : [
                                  "\u003ca href=\"https://maps.google.com/maps/contrib/113202928073475129698/photos\"\u003eEmily Zimny\u003c/a\u003e"
                               ],
                               "photo_reference" : "CmRaAAAAfxSORBfVmhZcERd-9eC5X1x1pKQgbmunjoYdGp4dYADIqC0AXVBCyeDNTHSL6NaG7-UiaqZ8b3BI4qZkFQKpNWTMdxIoRbpHzy-W_fntVxalx1MFNd3xO27KF3pkjYvCEhCd--QtZ-S087Sw5Ja_2O3MGhTr2mPMgeY8M3aP1z4gKPjmyfxolg",
                               "width" : 4032
                            }
                         ],
                         "rating": 4.3
                      }
                   ],
                   "debug_log": {
                      "line" : []
                   },
                   "status": "OK"
}

        mock_response = MockResponse()
        mock_candidate = mock_response.body['candidates'][0]
        mock_response.body = json.dumps(mock_response.body)
        cords = '53.429907,14.5501827'
        radius = 200
        spider = GooglePlacesSpider(cords=cords, radius=radius)
        gen = spider.parse(mock_response)

        item = next(gen)
        self.assertEqual(item['rating'], mock_candidate['rating'])

if __name__ == '__main__':
    unittest.main()
