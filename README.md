# Telemetry Ground Station

A PyQt5-based ground station interface for monitoring and testing telemetry packets transmitted from an embedded system (e.g., STM32) over a serial connection.

This application provides a graphical interface to visualize incoming telemetry data, inspect raw packet contents, and generate telemetry packets for testing purposes.

---

# Features

- Serial communication with telemetry devices (via USB / UART)
- Real-time visualization of telemetry data
- Packet parsing and display
- Raw packet byte inspection
- Telemetry packet generator for testing
- Clean PyQt5 graphical interface

---

# Project Status

The **receiver side is fully functional** and can read telemetry packets coming from the embedded system.

The **transmitter side is partially implemented** and currently serves as a testing interface for generating telemetry packets. It may require additional development for full integration with hardware transmission.

---

# Interface Overview

The interface is divided into three main sections:

## Receiver Panel

Displays telemetry values received from the embedded system.

Includes fields such as:

- Team ID
- Counter
- Altitude
- GPS coordinates
- Gyroscope values
- Acceleration values
- Angle
- State
- CRC

---

## Transmitter Panel

Allows manual entry of telemetry values and generation of telemetry packets.

Current capabilities:

- Manually edit telemetry values
- Generate a telemetry packet
- Inspect outgoing packet structure

⚠️ Note: Full transmitter functionality is still under development.

---

## Raw Packet Viewer

Displays the raw telemetry packet in hexadecimal format.

Example:

```
[FF][FF][54][52][01][05][...]
```

This helps debugging the packet format and verifying correct serialization.

---

# Packet Format

Telemetry packets follow a fixed-length binary structure.

Example layout:

| Byte Range | Description |
|-----------|-------------|
| 0–3 | Header |
| 4 | Team ID |
| 5 | Packet Counter |
| 6–33 | GPS and altitude data |
| 46–73 | IMU data |
| 74 | State |
| 75 | CRC |
| 76–77 | Packet ending |

All floating point values are encoded using IEEE-754 format.

---

# Requirements

Python 3.8+

Required libraries:

```
PyQt5
pyserial
```

Install dependencies:

```bash
pip install PyQt5 pyserial
```

---

# Running the Application

Run the application using:

```bash
python main.py
```

---

# Building an Executable

This project includes a PyInstaller configuration file.

To build a standalone executable:

```bash
pip install pyinstaller
pyinstaller app.spec
```

The compiled application will appear in the `dist` directory.

---

# Project Structure

```
telemetry-ground-station/
│
├── main.py
├── main_window.py
├── port_settings_window.py
├── packet_utils.py
├── serial_utils.py
├── app.spec
└── README.md
```

### Description

- **main.py** – application entry point  
- **main_window.py** – main GUI interface  
- **port_settings_window.py** – serial port configuration window  
- **packet_utils.py** – telemetry packet encoding/decoding  
- **serial_utils.py** – serial communication utilities  
- **app.spec** – PyInstaller build configuration  

---

# Possible Future Improvements

- Complete transmitter functionality
- CRC validation
- Automatic serial port detection
- Packet logging
- Data plotting (altitude, IMU, etc.)
- Telemetry recording

---

# License

This project is provided for educational and experimental purposes.

---

# Author

Developed as part of a telemetry ground station interface project.
