from datetime import datetime
import socket
import sys

class ConcreteClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.client_socket = None
        self.connected = False

    def connect_to_server(self):
        """Conectează clientul la server."""
        if self.connected:
            print("Sunteți deja conectat la server.")
            return
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.settimeout(5)  # Timeout de 5 secunde
            self.client_socket.connect((self.host, self.port))
            try:
                response = self.client_socket.recv(1024).decode()
                if not response:  # Dacă conexiunea este închisă imediat
                    print("Eroare: Serverul a închis conexiunea fără un răspuns.")
                    self.client_socket.close()
                elif response == "Serverul nu acceptă conexiuni noi.":
                    print("Eroare: Serverul nu acceptă conexiuni noi.")
                    self.client_socket.close()
                else:
                    self.connected = True
                    print("Conexiune stabilită cu serverul.")
                    print(f"Mesaj de la server: {response}")  # Print the welcome message
            except socket.timeout:
                print("Eroare: Timeout la așteptarea răspunsului de la server.")
                self.client_socket.close()
        except ConnectionRefusedError:
            print("Eroare: Serverul nu este pornit sau nu poate fi accesat.")
        except Exception as e:
            print("Eroare la conectarea cu serverul:", e)

    def disconnect_from_server(self):
        """Deconectează clientul de la server."""
        if not self.connected:
            print("Nu sunteți conectat la server.")
            return
        try:
            self.client_socket.close()
            self.connected = False
            print("Conexiune închisă.")
        except Exception as e:
            print("Eroare la deconectarea de la server:", e)

    def validate_date(self, date_str):
        """Validează local o dată calendaristică."""
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            today = datetime.today()

            if date.year < 1900:
                print("Eroare: Data este prea îndepărtată în trecut (an mai mic decât 1900).")
                return False
            if date > today:
                print("Eroare: Data este în viitor.")
                return False
            return True
        except ValueError:
            print("Eroare: Formatul datei este invalid. Folosiți formatul YYYY-MM-DD.")
            return False

    def send_date_to_server(self, date_str):
        """Trimite o dată calendaristică către server."""
        if not self.connected:
            print("Nu sunteți conectat la server. Conectați-vă înainte de a trimite o cerere.")
            return
        if not self.validate_date(date_str):
            return
        try:
            print(f"Cerere trimisă către server: {date_str}")
            self.client_socket.sendall(date_str.encode())
        except socket.timeout:
            print("Eroare: Timeout la așteptarea răspunsului de la server.")
            self.connected = False
        except Exception as e:
            print("Eroare la trimiterea cererii către server:", e)
            self.connected = False

    def receive_from_server(self):
        """Primește un mesaj de la server."""
        try:
            response = self.client_socket.recv(1024).decode()
            if response:
                print(f"Răspuns primit de la server: {response}")
            return response
        except socket.timeout:
            print("Eroare: Timeout la așteptarea răspunsului de la server.")
            return None
        except Exception as e:
            print("Eroare la primirea răspunsului:", e)
            return None

    def main_menu(self):
        """Afișează meniul principal pentru client."""
        while True:
            print("\nMeniu client:")
            print("1. Conectare la server")
            print("2. Deconectare de la server")
            print("3. Introducere dată calendaristică")
            print("4. Ieșire")
            option = input("Introduceți o opțiune (1-4): ")

            if option == "1":
                self.connect_to_server()
            elif option == "2":
                self.disconnect_from_server()
            elif option == "3":
                if not self.connected:
                    print("Nu sunteți conectat la server. Conectați-vă înainte de a trimite cereri.")
                    continue
                date_str = input("Introduceți data (format YYYY-MM-DD): ")
                self.send_date_to_server(date_str)
                self.receive_from_server()  # Receive and print the response
            elif option == "4":
                if self.connected:
                    self.disconnect_from_server()
                print("Ieșire din aplicație.")
                break
            else:
                print("Opțiune invalidă. Vă rugăm să introduceți un număr între 1 și 4.")

if __name__ == "__main__":
    client = ConcreteClient()
    client.main_menu()