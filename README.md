# OCSF-AgeCalculator

A client-server application for calculating age based on birth date, implemented following the Object Client-Server Framework (OCSF) architecture.

## Features

### Server
- Administrative menu with the following functionalities:
  - Start/stop the server
  - Activate/deactivate new client connections
  - Display current server status
- Multi-threaded design to handle multiple client connections simultaneously
- Detailed logging of server events (client connections, requests, responses)
- Connection management (accept/reject based on server status)

### Client
- User-friendly console menu interface
- Connect/disconnect from server
- Birth date input with validation
  - Format validation (YYYY-MM-DD)
  - Logic validation (not in future, year >= 1900)
- Detailed status messages
- Error handling for network issues and server disconnects

## Architecture

The application follows the OCSF architecture with:
- Abstract base classes defining the framework (AbstractServer, AbstractClient)
- Concrete implementations (ConcreteServer, ConcreteClient)
- Business logic classes (Person)
- Connection handling (ConnectionToClient)
- Test scenarios (test_scenario.py)

## Components

- `AbstractServer.py` - Base server framework
- `AbstractClient.py` - Base client framework
- `ConcreteServer.py` - Server implementation with admin menu
- `ConcreteClient.py` - Client implementation with user menu
- `ConnectionToClient.py` - Manages individual client connections
- `Person.py` - Core business logic for age calculation
- `test_scenario.py` - Automated test scenarios

## Installation & Usage

### Requirements
- Python 3.6 or higher
- No external dependencies required

### Running the Server
```bash
python ConcreteServer.py
```

### Running the Client
```bash
python ConcreteClient.py
```

### Running Tests
```bash
python test_scenario.py
```

## Test Scenario

The application has been tested with the following scenario:
1. Start server
2. Activate server connections
3. Connect client 1
4. Connect client 2
5. Client 1 sends invalid date
6. Client 1 sends valid date
7. Server responds to client 1
8. Client 2 sends valid date
9. Server responds to client 2
10. Deactivate server connections
11. Client 1 sends another valid date
12. Server responds to client 1
13. Client 3 attempts to connect (fails)
14. Client 2 sends another valid date
15. Server responds to client 2
16. Disconnect client 1
17. Shut down server
18. Handle connection loss for client 2

## Contributing

This project was developed as part of a laboratory assignment for demonstrating client-server architecture and OCSF implementation.

## License

[MIT License](LICENSE)
