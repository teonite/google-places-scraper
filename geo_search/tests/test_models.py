import unittest
import unittest.mock
from geo_search.models import BasePlaceModel
from geo_search.models import NearPlaceModel
import psycopg2
import json
import os


class BasePlaceModelTestCase(unittest.TestCase):

    def setUp(self):
        self.connection = psycopg2.connect(host="postgres", database="places",
                                           user="geoscraper", password="geoscraper")
        self.cursor = self.connection.cursor()

    def tearDown(self):
        self.cursor.execute("DROP TABLE base_places CASCADE;")
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def test_creating_base_place_table(self):
        """Check that calling class creates base_places table in database"""

        BasePlaceModel(self.connection)

        self.cursor.execute("SELECT exists(SELECT * FROM information_schema.tables WHERE table_name='base_places');")
        self.assertTrue(bool(self.cursor.fetchone()[0]))


    def test_save_data_to_database(self):
        """Check that save method saves Items into database"""

        reference = BasePlaceModel(self.connection)

        # Mock item
        item = {'base_coordinates': {'latitude': 53.4504331, 'longitude': 14.5340195}}
        coordinates = item['base_coordinates']

        reference.save(item)

        query = "SELECT EXISTS(SELECT base_place_id FROM base_places WHERE CAST(coordinates->>'latitude' AS FLOAT)=%s AND CAST(coordinates->>'longitude' AS FLOAT)=%s);"

        self.cursor.execute(query, (coordinates['latitude'], coordinates['longitude']))
        self.assertTrue(bool(self.cursor.fetchone()[0]))

    def test_get_id_method(self):
        """Check that get_id method returns any Id"""

        reference = BasePlaceModel(self.connection)
        mock_item = {'base_coordinates': {'latitude': 53.4504331, 'longitude': 14.5340195}}
        reference.save(mock_item)

        base_place_id = reference.get_id()
        self.assertIsNotNone(base_place_id)


class NearPlaceModelTestCase(unittest.TestCase):

    def setUp(self):
        self.connection = psycopg2.connect(host="postgres", database="places",
                                           user="geoscraper", password="geoscraper")
        self.cursor = self.connection.cursor()

    def tearDown(self):
        self.cursor.execute("DROP TABLE near_places;")
        self.cursor.execute("DROP TABLE base_places CASCADE;")
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def test_creating_near_place_table(self):
        """Check that calling NearPlace class creates near_places table in database"""

        NearPlaceModel(self.connection)

        self.cursor.execute("SELECT exists(SELECT * FROM information_schema.tables WHERE table_name='near_places');")
        self.assertTrue(bool(self.cursor.fetchone()[0]))

    def test_save_data_to_database(self):
        """Check that save method saves json data"""

        reference = NearPlaceModel(self.connection)
        # Mock item
        item = {'base_coordinates': {'latitude': 53.4504331, 'longitude': 14.5340195},
                'data': {"rating": 5, "name": "Technopark"}
                }
        reference.save(item)

        query = "SELECT EXISTS(SELECT near_place_id FROM near_places WHERE information->>'data'=%s);"
        self.cursor.execute(query, (json.dumps(item['data']),))
        self.assertTrue(bool(self.cursor.fetchone()[0]))


if __name__ == "__main__":
    unittest.main()
