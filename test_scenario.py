# File: test_scenario.py

import unittest
import threading
import time
from ConcreteServer import ConcreteServer
from ConcreteClient import ConcreteClient

class TestServerClientInteraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ConcreteServer()
        cls.server_thread = threading.Thread(target=cls.server.start_server)
        cls.server_thread.start()
        time.sleep(1)  # Allow server to start

    @classmethod
    def tearDownClass(cls):
        cls.server.stop_server()
        cls.server_thread.join()

    def setUp(self):
        self.client1 = ConcreteClient()
        self.client2 = ConcreteClient()
        self.client3 = ConcreteClient()

    def tearDown(self):
        self.client1.disconnect_from_server()
        self.client2.disconnect_from_server()
        self.client3.disconnect_from_server()

    def test_scenario(self):
        # Step 1: Start the server (already done in setUpClass)

        # Step 2: Activate the server
        self.server.activate_connections()

        # Step 3: Connect Client 1
        self.client1.connect_to_server()
        self.assertTrue(self.client1.connected)

        # Step 4: Connect Client 2
        self.client2.connect_to_server()
        self.assertTrue(self.client2.connected)

        # Step 5: Client 1 sends an invalid date
        self.client1.send_date_to_server("invalid-date")

        # Step 6: Client 1 sends a valid date
        self.client1.send_date_to_server("2000-01-01")
        time.sleep(1)  # Allow time for the server to respond

        # Step 7: Server responds to Client 1
        response = self.client1.receive_from_server()
        self.assertIn("Vârsta calculată este:", response)

        # Step 8: Client 2 sends a valid date
        self.client2.send_date_to_server("1990-05-15")
        time.sleep(1)  # Allow time for the server to respond

        # Step 9: Server responds to Client 2
        response = self.client2.receive_from_server()
        self.assertIn("Vârsta calculată este:", response)

        # Step 10: Stop the server from accepting new connections
        self.server.deactivate_connections()

        # Step 11: Client 1 sends another valid date
        self.client1.send_date_to_server("1985-12-25")
        time.sleep(1)  # Allow time for the server to respond

        # Step 12: Server responds to Client 1
        response = self.client1.receive_from_server()
        self.assertIn("Vârsta calculată este:", response)

        # Step 13: Client 3 attempts to connect (should fail)
        self.client3.connect_to_server()
        self.assertFalse(self.client3.connected)

        # Step 14: Client 2 sends another valid date
        self.client2.send_date_to_server("1975-07-20")
        time.sleep(1)  # Allow time for the server to respond

        # Step 15: Server responds to Client 2
        response = self.client2.receive_from_server()
        self.assertIn("Vârsta calculată este:", response)

        # Step 16: Disconnect Client 1
        self.client1.disconnect_from_server()
        self.assertFalse(self.client1.connected)

        # Step 17: Shut down the server
        self.server.stop_server()

        # Step 18: Handle the loss of connection for Client 2
        response = self.client2.receive_from_server()
        self.assertEqual(response, "Serverul se oprește.")

if __name__ == '__main__':
    unittest.main()