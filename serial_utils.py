import serial
from PyQt5.QtCore import pyqtSignal, QObject


class SerialOpenWorker(QObject):
    success = pyqtSignal(object, str) # ser objesi, mode 
    error = pyqtSignal(str) 
    finished = pyqtSignal()
    
    def __init__(self, port, baud, mode): 
        super().__init__() 
        self.port = port 
        self.baud = baud
        self.mode = mode 
        
    def run(self):
        try: 
            ser = serial.Serial(self.port, self.baud, timeout=1) 
            self.success.emit(ser, self.mode) 
        
        except serial.SerialException as e: 
            self.error.emit(str(e)) 
        
        finally: self.finished.emit()


def readFullPacket(ser):
        buffer = b""
        in_packet = False
        while True:
            if ser.in_waiting > 0:  # Check if there's data to read
                byte = ser.read(1)
                if byte == b"<":
                    if len(buffer) == 0 or len(buffer) >= 78:
                        buffer = b""  # Start of new packet
                        in_packet = True
                    else:
                        buffer += byte
                elif byte == b">" and in_packet:
                    if len(buffer) == 78:
                        return buffer  # End of packet, return the data
                    else:
                        buffer += byte
                elif in_packet:
                    buffer += byte