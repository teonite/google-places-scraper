import psycopg2
import json


class BasePlaceModel:
    """
    Model for base place data

    It takes Item, and connection as a parameters
    """

    def __init__(self, connection):

        self.connection = connection

        self.coordinates = None

        # Try to create table for data
        query = """ 
                    CREATE TABLE IF NOT EXISTS base_places (
                        base_place_id SERIAL PRIMARY KEY,
                        coordinates JSON NOT NULL
                    );
                    """
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            cursor.close()

    def save(self, item):
        """
        Save data into database
        :return:
        """

        self.coordinates = item['base_coordinates']

        query = """INSERT INTO base_places(coordinates) VALUES(%s);"""
        cursor = self.connection.cursor()

        try:
            cursor.execute(query, (json.dumps(self.coordinates),))
            self.connection.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        else:
            print("BasePlaceModel was saved to the database")

        finally:
            cursor.close()

    def get_id(self):
        """
        Get id of the object added by this model
        :return id of the place:
        """
        base_place_id = None

        cursor = self.connection.cursor()
        query = "SELECT base_place_id FROM base_places WHERE CAST(coordinates->>'latitude' AS FLOAT)=%s AND CAST(coordinates->>'longitude' AS FLOAT)=%s;"

        try:
            cursor.execute(query, (self.coordinates['latitude'], self.coordinates['longitude']))
            base_place_id = cursor.fetchone()
            self.connection.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        else:
            print("Pobieranie Id dziala")
        finally:
            cursor.close()
            print(f"returned id: {base_place_id}")
            return base_place_id


class NearPlaceModel:

    def __init__(self, connection):

        self.connection = connection

        # Create model for base place
        self.base_place = BasePlaceModel(self.connection)

        # Try to create table for data
        cursor = self.connection.cursor()
        query = """
            CREATE TABLE IF NOT EXISTS near_places (
                near_place_id SERIAL PRIMARY KEY,
                base_id INTEGER REFERENCES base_places(base_place_id),
                information JSON NOT NULL
            );
            """
        try:
            cursor.execute(query)
            self.connection.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        finally:
            cursor.close()

    def save(self, item):
        """Save item without base_place_coordinates into database

           It Create association between BasePlaceModel objects and NearPlacesModel objects
        """

        # Get the id based on coordinates passed to this class
        self.base_place_id = self.base_place.get_id()

        # if id of the base place does not exist
        if self.base_place_id is None:
            # Save data from model into database
            self.base_place.save(item)
            # Get id again
            self.base_place_id = self.base_place.get_id()

        # Delete property which is required only for BasePlace
        del item['base_coordinates']
        item_json = json.dumps(dict(item))

        cursor = self.connection.cursor()
        query = """INSERT INTO near_places(base_id, information) VALUES(%s, %s);"""

        try:
            cursor.execute(query, (self.base_place_id, item_json))
            self.connection.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        else:
            print("NearPlaceModel was saved to the database")
        finally:
            cursor.close()

