import unittest
import sethealth


class TestAPI(unittest.TestCase):
    def test_valid(self):
        client = sethealth.Client()
        token = client.getToken()
        self.assertGreater(len(token), 10)

    def test_valid_options(self):
        client = sethealth.Client()
        token = client.getToken(test_mode=True, user_id="user")
        self.assertGreater(len(token), 10)

    def test_unvalid(self):
        with self.assertRaises(sethealth.AuthException):
            client = sethealth.Client("", "")
            client.getToken()


if __name__ == "__main__":
    unittest.main()
