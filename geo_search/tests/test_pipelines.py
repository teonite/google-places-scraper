import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
from geo_search.spiders.google_places_spider import GooglePlacesSpider
from geo_search.items import Place
from geo_search.pipelines import PlacesPipeline


class SavingToDatabaseTestCase(unittest.TestCase):

    @patch('geo_search.pipelines.psycopg2')
    @patch('geo_search.pipelines.NearPlaceModel')
    def test_open_spider_create_connection(self, mock_near_place_model, mock_psycopg2):
        """Check that open_spider method set up new connection to the database"""
        # Instantiate real object
        reference = PlacesPipeline()
        # Call open_spider method
        reference.open_spider(spider=GooglePlacesSpider)
        # Check that connect method was called
        mock_psycopg2.connect.assert_called()

    @patch('geo_search.pipelines.psycopg2')
    @patch('geo_search.pipelines.NearPlaceModel')
    def test_saving_processed_item(self, mock_near_place_model, mock_psycopg2):
        """Check that process_item method calls save method on near_place object with item as a parametr"""

        # Instantiate Pipeline class
        reference = PlacesPipeline()

        # Mock the Item object
        item = unittest.mock.create_autospec(Place)
        # Mock near_place object and save method
        reference.near_place = MagicMock()
        reference.near_place.save = MagicMock()

        # Call method that call save method on instance of a NearPlaceModel class
        reference.process_item(item=item, spider=GooglePlacesSpider)

        reference.near_place.save.assert_called_with(item)

    @patch('geo_search.pipelines.psycopg2')
    @patch('geo_search.pipelines.NearPlaceModel')
    def test_closing_connection(self, mock_near_place_model, mock_psycopg2):
        """Check that close_spider method closes database connection"""

        # Instantiate real object
        reference = PlacesPipeline()

        # Mock connection attribute
        reference.connection = MagicMock()

        # Call close_spider method
        reference.close_spider(spider=GooglePlacesSpider)

        mock_connection = unittest.mock.create_autospec(reference.connection)
        mock_connection.close.assert_called()


if __name__ == '__main__':
    unittest.main()