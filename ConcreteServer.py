import socket
import threading
from AbstractServer import AbstractServer
from Person import Person
from ConnectionToClient import ConnectionToClient

class ConcreteServer(AbstractServer):
    def __init__(self, host='localhost', port=12345):
        super().__init__(host, port)
        self.is_running = False  # Serverul este inițial oprit
        self.is_active = False  # Conexiunile noi sunt inițial dezactivate

    def start_server(self):
        """Pornește serverul."""
        if self.is_running:
            print("Serverul este deja pornit.")
            return
        try:
            # Reinițializăm socket-ul serverului
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Set SO_REUSEADDR
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            self.is_running = True
            self.is_active = True
            print("Serverul a fost pornit și este activ pentru conexiuni.")

            # Fir separat pentru ascultare
            self.listen_thread = threading.Thread(target=self.listen, daemon=True)
            self.listen_thread.start()
        except Exception as e:
            print("Eroare la pornirea serverului:", e)

    def stop_server(self):
        """Oprește serverul și deconectează clienții."""
        if not self.is_running:
            print("Serverul nu este pornit.")
            return
        try:
            self.is_running = False
            # Informăm clienții înainte de a închide conexiunile
            for connection in self.clients[:]:
                try:
                    connection.send_to_client("Serverul se oprește.")
                except Exception as e:
                    print(f"Eroare la trimiterea mesajului către {connection.client_address}: {e}")
                connection.stop()
            self.clients = []  # Golește lista de clienți
            self.server_socket.close()
            print("Serverul a fost oprit.")
        except Exception as e:
            print("Eroare la oprirea serverului:", e)
        finally:
            if self.server_socket:
                self.server_socket.close()


    def activate_connections(self):
        """Activează conexiunile noi."""
        if not self.is_running:
            print("Serverul nu este pornit.")
            return
        if self.is_active:
            print("Conexiunile pentru clienți sunt deja activate.")
            return
        self.is_active = True
        print("Conexiunile pentru clienți au fost activate.")

    def deactivate_connections(self):
        """Dezactivează conexiunile noi."""
        if not self.is_running:
            print("Serverul nu este pornit.")
            return
        if not self.is_active:
            print("Conexiunile pentru clienți sunt deja dezactivate.")
            return
        self.is_active = False
        print("Conexiunile pentru clienți au fost dezactivate.")

    def show_status(self):
        """Afișează starea curentă a serverului."""
        if not self.is_running:
            print("Serverul este oprit.")
            return
        print(f"Serverul este pornit.")
        print(f"Conexiuni noi: {'activate' if self.is_active else 'dezactivate'}")
        print(f"Clienți conectați: {len(self.clients)}")
        if self.clients:
            print("Lista clienților:")
            for client in self.clients:
                print(f" - {client.client_address}")



    def handle_message_from_client(self, connection, birth_date_str):
        """Preia mesajul primit de la client și procesează cererea."""
        try:
            person = Person(birth_date_str)
            age = person.get_age()

            if age is not None:
                response = f"Vârsta calculată este: {age} ani."
                print(f"Trimiterea răspunsului către client {connection.client_address}: {response}")
            else:
                response = "Data introdusă este invalidă."
                print(f"Data introdusă de client {connection.client_address} este invalidă.")

            connection.send_to_client(response)
        except Exception as e:
            print(f"Eroare la procesarea mesajului de la client {connection.client_address}: {e}")
            connection.send_to_client("Eroare la procesarea cererii. Încercați din nou.")


    def listen(self):
        """Ascultă conexiunile client și creează un fir de execuție pentru fiecare client."""
        print("Serverul este acum în ascultare pe portul", self.port)
        while self.is_running:
            try:
                client_socket, client_address = self.server_socket.accept()
                if not self.is_active:
                    print(f"Conexiunea clientului {client_address} a fost respinsă – server dezactivat.")
                    try:
                        client_socket.sendall("Serverul nu acceptă conexiuni noi.".encode())
                    except Exception as e:
                        print(f"Eroare la trimiterea mesajului de respingere către {client_address}: {e}")
                    finally:
                        client_socket.close()
                    continue
                print("Client conectat:", client_address)
                client_socket.sendall("Bine ați venit la server!".encode())  # Send welcome message
                connection = ConnectionToClient(client_socket, client_address, self)
                connection.start()
                self.clients.append(connection)
            except OSError:
                break

    def admin_menu(self):
        """Meniu de administrare pentru server."""
        while True:
            print("\nMeniu administrare server:")
            print("1. Pornește serverul")
            print("2. Oprește serverul")
            print("3. Activează conexiunile pentru clienți")
            print("4. Dezactivează conexiunile pentru clienți")
            print("5. Afișează starea curentă")
            print("6. Ieșire")
            option = input("Introduceți o opțiune (1-6): ")

            if option == "1":
                self.start_server()
            elif option == "2":
                self.stop_server()
            elif option == "3":
                self.activate_connections()
            elif option == "4":
                self.deactivate_connections()
            elif option == "5":
                self.show_status()
            elif option == "6":
                if self.is_running:
                    self.stop_server()
                print("Ieșire din administrare.")
                break
            else:
                print("Opțiune invalidă. Vă rugăm să introduceți un număr între 1 și 6.")


if __name__ == "__main__":
    server = ConcreteServer()
    server.admin_menu()
