from devices import BaseDevice, HomeSensor, CleaningSensor, LightSensor

class WebInterface:
    def __init__(self, devices):
        self.devices = devices

    def display_dashboard(self):
        print("\n--- Web Interface Dashboard ---")
        for device in self.devices:
            if isinstance(device, HomeSensor):
                print(f"{device.name}: {device.read_data()}")
            elif isinstance(device, CleaningSensor):
                print(f"{device.name}: {device.detect_dirt()}")
            elif isinstance(device, LightSensor):
                print(f"{device.name}: {device.measure_light()}")
            else:
                print(f"{device.name}: No data available")

    def control_devices(self, device_name, command):
        for device in self.devices:
            if device.name == device_name:
                if isinstance(device, HomeSensor):
                    if command == "calibrate":
                        # Simulate calibration (replace with actual calibration logic)
                        print(f"Calibrating {device.name}")
                    else:
                        print(f"Invalid command for {device.name}")
                elif isinstance(device, CleaningSensor):
                    if command == "start":
                        device.status = True
                        print(f"Starting {device.name}")
                    elif command == "stop":
                        device.status = False
                        print(f"Stopping {device.name}")
                    else:
                        print(f"Invalid command for {device.name}")
                elif isinstance(device, LightSensor):
                    if command == "adjust":
                        # Simulate light adjustment (replace with actual adjustment logic)
                        print(f"Adjusting {device.name}")
                    else:
                        print(f"Invalid command for {device.name}")
                break
        else:
            print(f"Device '{device_name}' not found.")

class MobileInterface:
    def __init__(self, devices):
        self.devices = devices

    def display_dashboard(self):
        print("\n--- Mobile Interface Dashboard ---")
        for device in self.devices:
            if isinstance(device, HomeSensor):
                print(f"{device.name}: {device.read_data()}")
            elif isinstance(device, CleaningSensor):
                print(f"{device.name}: {device.detect_dirt()}")
            elif isinstance(device, LightSensor):
                print(f"{device.name}: {device.measure_light()}")
            else:
                print(f"{device.name}: No data available")

    def control_devices(self, device_name, command):
        for device in self.devices:
            if device.name == device_name:
                if isinstance(device, HomeSensor):
                    if command == "calibrate":
                        # Simulate calibration (replace with actual calibration logic)
                        print(f"Calibrating {device.name}")
                    else:
                        print(f"Invalid command for {device.name}")
                elif isinstance(device, CleaningSensor):
                    if command == "start":
                        device.status = True
                        print(f"Starting {device.name}")
                    elif command == "stop":
                        device.status = False
                        print(f"Stopping {device.name}")
                    else:
                        print(f"Invalid command for {device.name}")
                elif isinstance(device, LightSensor):
                    if command == "adjust":
                        # Simulate light adjustment (replace with actual adjustment logic)
                        print(f"Adjusting {device.name}")
                    else:
                        print(f"Invalid command for {device.name}")
                break
        else:
            print(f"Device '{device_name}' not found.")