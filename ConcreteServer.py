from AbstractServer import AbstractServer
from Person import Person
from ConnectionToClient import ConnectionToClient
import threading

class ConcreteServer(AbstractServer):
    def handle_message_from_client(self, connection, birth_date_str):
        """Preia mesajul primit de la client și procesează cererea."""
        person = Person(birth_date_str)
        age = person.get_age()

        if age is not None:
            response = f"Vârsta calculată este: {age} ani."
            print("Trimiterea vârstei către client:", response)
        else:
            response = "Data introdusă este invalidă."
            print("Data introdusă de client este invalidă.")

        connection.send_to_client(response)

    def listen(self):
        """Ascultă conexiunile client și creează un fir de execuție pentru fiecare client."""
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            self.is_listening = True
            print("Serverul este acum în ascultare pe portul", self.port)

            # Fir separat pentru a asculta comanda de oprire
            threading.Thread(target=self.await_stop_command, daemon=True).start()

            while self.is_listening:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print("Client conectat:", client_address)

                    connection = ConnectionToClient(client_socket, client_address, self)
                    connection.start()
                    self.clients.append(connection)
                except OSError:
                    # Ignorăm eroarea dacă socket-ul a fost închis
                    break
        except Exception as e:
            print("Eroare la ascultare:", e)

    def stop_listening(self):
        """Oprește serverul în mod controlat."""
        self.is_listening = False
        try:
            self.server_socket.close()  # Închidem socket-ul pentru a opri ascultarea
        except Exception as e:
            print("Eroare la închiderea socket-ului serverului:", e)

        for connection in self.clients:
            connection.stop()
        print("Serverul a fost oprit.")

    def await_stop_command(self):
        """Ascultă comanda 'quit' fără să afișeze un prompt."""
        while self.is_listening:
            command = input().strip().lower()
            if command == "quit":
                self.stop_listening()

if __name__ == "__main__":
    server = ConcreteServer()
    server.listen()
