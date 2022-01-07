try: 
    from app import app
    import unittest

except Exception as e:
    print("Some Modules are Missing {} ".format(e))
import json

class FlaskTest(unittest.TestCase):

    # Prüfe ob Statuscode 200 zurückgegeben wird
    def test_movies_get(self):
        tester = app.test_client(self)
        response = tester.get("/movies")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    # Prüfe, ob der zurückgegebene Wert vom Typ JSON ist
    def test_movies_return_type(self):
        tester = app.test_client(self)
        response = tester.get("/movies")
        self.assertEqual(response.content_type, "application/json")

    # Prüfe, ob der Request POST den Statuscode 201 zurückgibt
    def test_movies_post(self):
        tester = app.test_client(self)
        response = tester.post("/movies", data=dict(
            director="test_director",
            genre="test_genre",
            title="test_title"
        ))
        statuscode = response.status_code
        self.assertEqual(statuscode, 201)



if __name__ == "__main__":
    unittest.main()