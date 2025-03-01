# Age-Calculator-OCSF

A client-server application that calculates a person's age in completed years based on their birth date, following the Object Client-Server Framework (OCSF) architecture.

## Description

This application demonstrates a simple client-server architecture where:
- The client asks the user for their birth date
- The server calculates the age in years
- The result is returned to the client and displayed

The implementation follows the OCSF pattern with abstract base classes that are extended by concrete implementations.

## Features

- Multithreaded server that can handle multiple clients simultaneously
- Birth date validation on both client and server sides
- Support for leap years in age calculation
- Graceful error handling for network issues
- Unit and integration tests

## Project Structure

- `AbstractClient.py` - Base class for client implementation with socket handling
- `AbstractServer.py` - Base class for server implementation with threading support
- `ConcreteClient.py` - Client application that gets user input and displays results
- `ConcreteServer.py` - Server application that processes birth dates and calculates ages
- `ConnectionToClient.py` - Handles individual client connections on the server
- `Person.py` - Core business logic for age calculation
- `test_bench.py` - Comprehensive test suite

## Requirements

- Python 3.6 or higher
- No external dependencies required (uses only standard library)

## Usage

### Running the Server

```bash
python ConcreteServer.py
```

The server will start listening on port 12345. Type `quit` to stop the server.

### Running the Client

```bash
python ConcreteClient.py
```

Enter your birth date in the format YYYY-MM-DD when prompted.

## Testing

Run the comprehensive test suite with:

```bash
python test_bench.py
```

This includes unit tests for the Person and ConcreteClient classes, as well as integration tests for client-server communication.

## Class Diagram

The application follows this class structure:

- AbstractServer (base class)
  - ConcreteServer (implementation)
  - ConnectionToClient (handles client connections)
  - Person (calculates age)

- AbstractClient (base class)
  - ConcreteClient (implementation)

## License

MIT License
