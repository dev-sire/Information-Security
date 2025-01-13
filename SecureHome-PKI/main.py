from devices import HomeSensor, CleaningSensor, LightSensor
from network import WirelessNetwork
import ui

# Replace with actual server address and certificate path
server_address = "192.168.0.7"
server_certificate_path = "/server.crt"

# Create devices
home_sensor = HomeSensor("TemperatureSensor", "Temperature", "Celsius")
cleaning_sensor = CleaningSensor("Cleaning Sensor")
light_sensor = LightSensor("Light Sensor")

# Create network and connect devices
network = WirelessNetwork(server_address, server_certificate_path)
network.connect_device(home_sensor)
network.connect_device(cleaning_sensor)
network.connect_device(light_sensor)

# Create web interface instance
web_interface = ui.WebInterface([home_sensor, cleaning_sensor, light_sensor])

# Function to send command to a device using UI
def send_command_to_device(device_name, command):
    network.send_command_to_device(device_name, command)

# Main loop
while True:
    # Web interface interaction
    web_interface.display_dashboard()
    device_name = input("Enter device name (or 'exit' to quit): ")
    if device_name.lower() == "exit":
        break
    command = input("Enter command (calibrate, start, stop, adjust, or 'back' to go back): ")
    if command.lower() == "back":
        continue

    # Send command to device (if valid)
    if device_name and command:
        send_command_to_device(device_name, command)
    else:
        print("Invalid input. Please enter a device name and command.")