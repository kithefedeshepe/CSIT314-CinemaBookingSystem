from pymongo import MongoClient
from django.test import SimpleTestCase
from pymongo.errors import ConnectionFailure

class TestDB(SimpleTestCase):
    def test_db_con(self):
        try:
            client = MongoClient("mongodb+srv://bsian314:bsian314@bsian.lzgtcdx.mongodb.net/test", username="bsian314", password="bsian314")
            db = client.test
            assert db.command("ping")
        except ConnectionFailure:
            self.fail("Failed to connect to MongoDB Atlas cluster")
