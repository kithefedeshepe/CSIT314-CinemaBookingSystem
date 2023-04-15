from pymongo import MongoClient
from django.test import SimpleTestCase

class TestDB(SimpleTestCase):
    def test_db_con(self):
        client = MongoClient("mongodb+srv://bsian314:bsian314@bsian.lzgtcdx.mongodb.net/test", username="bsian314", password="bsian314")
        db = client.test
        assert db.command("ping")['ok'] == 1.0, "Database connection error"


