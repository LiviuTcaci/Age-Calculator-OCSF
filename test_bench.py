import unittest
from datetime import datetime
from Person import Person  # Clasa Person creată pentru calculul vârstei
from ConcreteClient import ConcreteClient  # Presupunem că are funcția validate_birth_date
from ConcreteServer import ConcreteServer
import threading
import socket

class TestPerson(unittest.TestCase):
    def test_age_calculation_normal(self):
        person = Person("2000-05-20")
        expected_age = datetime.today().year - 2000
        if (datetime.today().month, datetime.today().day) < (5, 20):
            expected_age -= 1
        self.assertEqual(person.get_age(), expected_age)

    def test_age_calculation_leap_year(self):
        person = Person("2000-02-29")
        expected_age = datetime.today().year - 2000
        if (datetime.today().month, datetime.today().day) < (2, 29):
            expected_age -= 1
        self.assertEqual(person.get_age(), expected_age)

    def test_invalid_date(self):
        person = Person("2023-02-30")
        self.assertIsNone(person.get_age())

    def test_future_date(self):
        future_date = datetime.today().replace(year=datetime.today().year + 1).strftime("%Y-%m-%d")
        person = Person(future_date)
        self.assertIsNone(person.get_age())


class TestConcreteClient(unittest.TestCase):
    def setUp(self):
        self.client = ConcreteClient()

    def test_validate_date_correct_format(self):
        self.assertTrue(self.client.validate_birth_date("2000-05-20"))

    def test_validate_date_incorrect_format(self):
        self.assertFalse(self.client.validate_birth_date("20-05-2000"))

    def test_validate_date_future(self):
        future_date = datetime.today().replace(year=datetime.today().year + 1).strftime("%Y-%m-%d")
        self.assertFalse(self.client.validate_birth_date(future_date))

    def test_validate_date_leap_year(self):
        self.assertTrue(self.client.validate_birth_date("2000-02-29"))

    def test_validate_date_invalid(self):
        self.assertFalse(self.client.validate_birth_date("2023-02-30"))


class TestServerClientIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ConcreteServer()
        cls.server_thread = threading.Thread(target=cls.server.listen)
        cls.server_thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop_listening()
        cls.server_thread.join()

    def connect_and_send(self, date):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))
        client_socket.sendall(date.encode())
        response = client_socket.recv(1024).decode()
        client_socket.close()
        return response

    def test_integration_valid_date(self):
        response = self.connect_and_send("2000-05-20")
        self.assertIn("Vârsta calculată este:", response)

    def test_integration_leap_year(self):
        response = self.connect_and_send("2000-02-29")
        self.assertIn("Vârsta calculată este:", response)

    def test_integration_invalid_date(self):
        response = self.connect_and_send("2023-02-30")
        self.assertIn("Data introdusă este invalidă.", response)

    def test_integration_future_date(self):
        future_date = datetime.today().replace(year=datetime.today().year + 1).strftime("%Y-%m-%d")
        response = self.connect_and_send(future_date)

    def test_multiple_clients(self):
        responses = []
        future_date = datetime.today().replace(year=datetime.today().year + 1).strftime(
            "%Y-%m-%d")  # Adăugăm future_date
        dates = ["2000-05-20", "2000-02-29", "2023-02-30", future_date]
        threads = []

        for date in dates:
            thread = threading.Thread(target=lambda d=date: responses.append(self.connect_and_send(d)))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.assertTrue(any("Vârsta calculată este:" in r for r in responses))
        self.assertTrue(any("Data introdusă este invalidă." in r for r in responses))



if __name__ == "__main__":
    unittest.main()
