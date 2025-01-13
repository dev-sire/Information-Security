import socket

HOST = 'localhost'
PORT = 9090

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("=====================================================")
    print(f"|             CLIENT CONNECTED WITH PORT {PORT}             |")
    print("=====================================================")
    while True:
        try:
            message = input("Enter a command: ")
            if message.lower() == 'exit':
                break
            s.sendall(message.encode())
            data = s.recv(1024)
            print(f"Received from server: {data.decode()}")

            if message.startswith('sudo') or message.startswith('DROP TABLE'):
                print("Intrusive command sent.")
            else:
                print("Command sent successfully.")

        except KeyboardInterrupt:
            print("\nExiting client...")
            break