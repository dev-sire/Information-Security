import socket
import logging

logging.basicConfig(filename='security.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Define a list of intrusive commands
intrusive_commands = [
    "sudo", 
    "su", 
    "root", 
    "rm -rf", 
    "rm -r", 
    "del /f /q /s", 
    "format", 
    "shutdown", 
    "reboot", 
    "drop table", 
    "truncate table", 
    "delete from", 
    "insert into", 
    "update", 
    "alter table", 
    "grant all privileges", 
    "net user", 
    "whoami /priv", 
    "tasklist /v", 
    "ipconfig /all", 
    "ping", 
    "traceroute", 
    "telnet", 
    "netcat", 
    "nmap" 
]

def handle_client(conn, addr):
    print(f"\n\n==============================> Connection established with {addr} <==============================")
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f"Received command: {data}")

            is_intrusive = False
            for command in intrusive_commands:
                if command in data.lower():
                    is_intrusive = True
                    break

            if is_intrusive:
                logging.info(f"server: Intrusive command detected: {data}")
                conn.sendall(b"Intrusive command.\n") 
            else:
                conn.sendall(b"Command executed successfully.\n") 

        except Exception as e:
            print(f"Error handling client: {e}")
            break
    conn.close()
    print(f"\n\n=========================> Connection closed with {addr} <=========================")

def main():
    host = 'localhost'
    port = 9090

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"\n\n==============================> Server listening on {host}:{port} <==============================") 
        conn, addr = s.accept()
        handle_client(conn, addr)

if __name__ == '__main__':
    main()