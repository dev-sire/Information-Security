from devices import HomeSensor, CleaningSensor, LightSensor
from network import WirelessNetwork
import ui

server_address = ('localhost', 5000)
server_certificate_path = "server.crt"

home_sensor = HomeSensor("TemperatureSensor", "Temperature", "Celsius", "localhost", 8081)
cleaning_sensor = CleaningSensor("CleaningSensor", "localhost", 8082)
light_sensor = LightSensor("LightSensor", "localhost", 8083)

# Create network and connect devices
network = WirelessNetwork(server_address, server_certificate_path)  

try:
    network.connect_device(home_sensor)
    network.connect_device(cleaning_sensor)
    network.connect_device(light_sensor)
except Exception as e:
    print(f"Error connecting devices: {e}")
    exit(1)

web_interface = ui.WebInterface([home_sensor, cleaning_sensor, light_sensor])

def send_command_to_device(device_name, command):
    try:
        network.send_command_to_device(device_name, command)
    except Exception as e:
        print(f"Error sending command to {device_name}: {e}")

while True:
    web_interface.display_dashboard()
    device_name = input("Enter device name (or 'exit' to quit): ")
    if device_name.lower() == "exit":
        break
    command = input("Enter command (calibrate, start, stop, adjust, or 'back' to go back): ")
    if command.lower() == "back":
        continue

    if device_name and command:
        send_command_to_device(device_name, command)
    else:
        print("Invalid input. Please enter a device name and command.")