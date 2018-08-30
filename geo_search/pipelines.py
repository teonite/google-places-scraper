from .models import NearPlaceModel
import psycopg2
from geo_search.settings import DB_PARAMS


class PlacesPipeline(object):

    def open_spider(self, spider):

        # Try connect to the database
        self.connection = None
        try:
            print("Connecting to the database")
            self.connection = psycopg2.connect(**DB_PARAMS)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        self.near_place = NearPlaceModel(self.connection)

    def process_item(self, item, spider):

        # Create NearPlace model based on item and save it into db
        self.near_place.save(item)
        return item

    def close_spider(self, spider):
        """
        This method is executed when the spider is closed
        So this method closes database connection
        """

        self.connection.close()

