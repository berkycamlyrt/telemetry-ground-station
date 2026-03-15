from PyQt5.QtWidgets import QWidget, QPushButton, QDesktopWidget, QLabel, QLineEdit, QMessageBox, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QFrame, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer, QThread
from port_settings_window import PortSettingWindow
from serial_utils import SerialOpenWorker, readFullPacket
from packet_utils import parsePacket, buildPacketFromInputs, packetToHexStrings


DEBUG = False
BOX_AROUND_DATA = False


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initVariables()

        # self.setupDimensions()
        # self.setupPositions()
        # self.setupLabels()
        # self.setupButtons()
        # self.setupWindow()
        self.setupUi()
        
        self.setupTimer()
           

    def initVariables(self):
        self.arduino_port = ""
        self.baud = 0

        self.setWindowTitle("App")
        self.font = QFont("Consolas", 13)

        self.start_receiver = False
        self.start_transmitter = False

        self.serial_opened = False
        self.serial_buffer = bytearray()


        self.screen = QDesktopWidget().screenGeometry()
        self.r_labels = []
        self.t_labels = []
        self.d_labels = []
        self.packet = bytearray(78)

        self.test_label_names1 = ["Team ID:", "Counter:", "Altitude:", "Rocket GPS Altitude:", "Rocket Latitude:", "Rocket Longitude:",
                               "Payload GPS Altitude:", "Payload Latitude:", "Payload Longitude:"]
        self.test_label_names2 = ["Gyroscope X:", "Gyroscope Y:", "Gyroscope Z:", "Acceleration X:", "Acceleration Y:", "Acceleration Z:", "Angle:", "State:", "CRC:"]

        self.data_label_names = ["INCOMING 1:", "INCOMING 2:", "OUTGOING 3:", "OUTGOING 4:"]


    def setupUi(self):
        self.setWindowTitle("App")
        self.resize(1400, 800)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)

        # Top part
        top_layout = QHBoxLayout()
        top_layout.setSpacing(12)
        main_layout.addLayout(top_layout, 3)

        # Bottom part
        bottom_layout = QGridLayout()
        bottom_layout.setHorizontalSpacing(12)
        bottom_layout.setVerticalSpacing(10)
        main_layout.addLayout(bottom_layout, 1)

        # Panels
        settings_group = self.createSettingsPanel()
        receiver_group = self.createReceiverPanel()
        transmitter_group = self.createTransmitterPanel()

        top_layout.addWidget(settings_group, 1)
        top_layout.addWidget(receiver_group, 3)
        top_layout.addWidget(transmitter_group, 3)

        # Bottom data area
        self.createBottomPanel(bottom_layout)


    def createSettingsPanel(self):
        group = QGroupBox()
        group.setTitle("Settings")
        group.setFont(self.font)

        outer_layout = QVBoxLayout(group)
        outer_layout.setContentsMargins(12, 12, 12, 12)
        outer_layout.setSpacing(14)

        # Receiver title
        self.label_r_set = QLabel("Receiver Settings")
        self.label_r_set.setFont(self.font)
        outer_layout.addWidget(self.label_r_set)

        # Receiver buttons container
        receiver_buttons_layout = QVBoxLayout()
        receiver_buttons_layout.setSpacing(12)

        self.r_ps_button = QPushButton("Port Settings")
        self.r_op_button = QPushButton("Open Port")

        for btn in (self.r_ps_button, self.r_op_button):
            btn.setFont(self.font)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setMinimumHeight(60)

        self.r_ps_button.clicked.connect(lambda: self.setPortSettings("r"))
        self.r_op_button.clicked.connect(lambda: self.openPort("r"))

        receiver_buttons_layout.addWidget(self.r_ps_button, 1)
        receiver_buttons_layout.addWidget(self.r_op_button, 1)

        outer_layout.addLayout(receiver_buttons_layout, 2)

        # spacing between sections
        outer_layout.addSpacing(5)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        outer_layout.addWidget(line)

        outer_layout.addSpacing(5)

        # Transmitter title
        self.label_t_set = QLabel("Transmitter Setting")
        self.label_t_set.setFont(self.font)
        outer_layout.addWidget(self.label_t_set)

        # Transmitter buttons container
        transmitter_buttons_layout = QVBoxLayout()
        transmitter_buttons_layout.setSpacing(12)

        self.t_ps_button = QPushButton("Port Settings")
        self.t_op_button = QPushButton("Open Port")
        self.t_send_button = QPushButton("Send")

        for btn in (self.t_ps_button, self.t_op_button, self.t_send_button):
            btn.setFont(self.font)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setMinimumHeight(60)

        self.t_ps_button.clicked.connect(lambda: self.setPortSettings("t"))
        self.t_op_button.clicked.connect(lambda: self.openPort("t"))
        self.t_send_button.clicked.connect(self.onSendButtonClick)

        transmitter_buttons_layout.addWidget(self.t_ps_button, 1)
        transmitter_buttons_layout.addWidget(self.t_op_button, 1)
        transmitter_buttons_layout.addWidget(self.t_send_button, 1)

        outer_layout.addLayout(transmitter_buttons_layout, 3)

        return group


    def createReceiverPanel(self):
        group = QGroupBox("Receiver Test")
        group.setFont(self.font)

        grid = QGridLayout(group)
        grid.setContentsMargins(10, 10, 10, 10)
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(8)

        self.r_labels = []

        for i in range(9):
            row_widgets = []

            texts = [
                self.test_label_names1[i],
                "0",
                self.test_label_names2[i],
                "0"
            ]

            for j in range(4):
                label = QLabel(texts[j])
                label.setFont(self.font)

                if j in (1, 3):
                    if BOX_AROUND_DATA:
                        label.setFrameShape(QFrame.Box)
                    label.setMinimumWidth(90)

                grid.addWidget(label, i, j)
                row_widgets.append(label)

            self.r_labels.append(row_widgets)

        grid.setColumnStretch(0, 2)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 2)
        grid.setColumnStretch(3, 1)

        return group


    def createTransmitterPanel(self):
        group = QGroupBox("Transmitter Test")
        group.setFont(self.font)

        grid = QGridLayout(group)
        grid.setContentsMargins(10, 10, 10, 10)
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(8)

        self.t_labels = []

        for i in range(9):
            row_widgets = []

            for j in range(4):
                if j == 0:
                    widget = QLabel(self.test_label_names1[i])
                elif j == 2:
                    widget = QLabel(self.test_label_names2[i])
                elif j in (1, 3):
                    widget = QLineEdit("0")
                    widget.setFont(self.font)
                    widget.setMinimumWidth(90)
                else:
                    widget = QLabel("0")

                widget.setFont(self.font)
                grid.addWidget(widget, i, j)
                row_widgets.append(widget)

            self.t_labels.append(row_widgets)

        self.t_labels[0][1].setReadOnly(True)

        grid.setColumnStretch(0, 2)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 2)
        grid.setColumnStretch(3, 1)

        return group


    def createBottomPanel(self, bottom_layout):
        self.d_labels = []

        for i in range(4):
            title = QLabel(self.data_label_names[i])
            title.setFont(self.font)

            value = QLabel("Empty")
            value.setFont(self.font)
            
            if BOX_AROUND_DATA:
                value.setFrameShape(QFrame.Box)
            
            value.setWordWrap(True)
            value.setMinimumHeight(40)

            bottom_layout.addWidget(title, i, 0)
            bottom_layout.addWidget(value, i, 1)

            self.d_labels.append([title, value])

        bottom_layout.setColumnStretch(0, 1)
        bottom_layout.setColumnStretch(1, 6)


    def setupTimer(self):
        self.timer = QTimer(self)
        if self.start_receiver or self.start_transmitter:
            self.timer.timeout.connect(self.updateData)
            self.timer.start(100)


    def collectTransmitterInputs(self):
        return {
            "team_id": int(self.t_labels[0][1].text()).to_bytes(1, byteorder='little')[0],
            "counter": int(self.t_labels[1][1].text()).to_bytes(1, byteorder='little')[0],
            "altitude": float(self.t_labels[2][1].text()),
            "rocket_gps_altitude": float(self.t_labels[3][1].text()),
            "rocket_latitude":  float(self.t_labels[4][1].text()),
            "rocket_longitude": float(self.t_labels[5][1].text()),
            "payload_gps_altitude": float(self.t_labels[6][1].text()),
            "payload_latitude": float(self.t_labels[7][1].text()),
            "payload_longitude": float(self.t_labels[8][1].text()),
            "gyro_x": float(self.t_labels[0][3].text()),
            "gyro_y": float(self.t_labels[1][3].text()),
            "gyro_z": float(self.t_labels[2][3].text()),
            "acceleration_x": float(self.t_labels[3][3].text()),
            "acceleration_y": float(self.t_labels[4][3].text()),
            "acceleration_z": float(self.t_labels[5][3].text()),
            "angle": float(self.t_labels[6][3].text()),
            "state": int(self.t_labels[7][3].text()).to_bytes(1, byteorder='little')[0],
            "crc": int(self.t_labels[8][3].text()).to_bytes(1, byteorder='little')[0],
        }


    def updateTransmitterAndReceiverFromData(self, data_packet, r_or_t):
        labels = parsePacket(data_packet)

        for i in range(9):
            for j in range(2):
                idx2 = 2 * j + 1
                text = str(labels[j][i])
                if (r_or_t == "r"):
                    self.r_labels[i][idx2].setText(text)
                else:
                    if not (((i == 0 or i == 1) and j == 0) or ((i == 7 or i == 8) and j == 1)):    
                        text_val = float(text)
                        text = f"{text_val:.5f}"
                    self.t_labels[i][idx2].setText(text)

        first_part_str, second_part_str = packetToHexStrings(data_packet)


        if r_or_t == "r":
            self.d_labels[0][1].setText(first_part_str)
            self.d_labels[1][1].setText(second_part_str)
        elif r_or_t == "t":
            self.d_labels[2][1].setText(first_part_str)
            self.d_labels[3][1].setText(second_part_str)


    def onSendButtonClick(self):
        self.packet = buildPacketFromInputs(self.collectTransmitterInputs())

        # Giden alanlarını güncelle
        self.updateTransmitterAndReceiverFromData(self.packet, "t")

        # İstersen receiver tarafını da aynı veriyle test amaçlı güncelle
        self.updateTransmitterAndReceiverFromData(self.packet, "r")
                    

    def updateData(self):
        # send data to receiver
        if self.start_receiver:
            if DEBUG:
                print("in_waiting =", self.ser.in_waiting)
            packet = readFullPacket(self.ser)
            if packet:
                if DEBUG:
                    print("PACKET RECEIVED")
                self.packet = packet
                self.updateTransmitterAndReceiverFromData(packet, "r")
        # get data from the packet
        if self.start_transmitter:
            self.packet = readFullPacket(self.ser)
            if self.packet:
                self.updateTransmitterAndReceiverFromData(self.packet, "t")


    def openPort(self, r_or_t):
        if self.arduino_port == "":
            QMessageBox.critical(self, "Error", "Arduino Port is not Set!") 
            return 
        
        if self.baud == 0: 
            QMessageBox.critical(self, "Error", "Baud is not Set!") 
            return 
        
        if r_or_t not in ("r", "t"): 
            QMessageBox.critical(self, "Error", "Invalid mode! Use 'r' or 't'.") 
            return 
        
        if self.serial_opened: 
            if r_or_t == "r":
                self.start_receiver = True 
            
            elif r_or_t == "t": 
                self.start_transmitter = True 
            
            if not getattr(self, "_timer_connected", False): 
                self.timer.timeout.connect(self.updateData) 
                self._timer_connected = True 
                
                if not self.timer.isActive():
                    self.timer.start(500)
                    QMessageBox.information(self, "Info", "Port already opened.") 
                    return 
        
        self.open_thread = QThread() 
        self.open_worker = SerialOpenWorker(self.arduino_port, self.baud, r_or_t) 
        self.open_worker.moveToThread(self.open_thread)
        self.open_thread.started.connect(self.open_worker.run)
        self.open_worker.success.connect(self.onPortOpened)
        self.open_worker.error.connect(self.onPortOpenError)
        self.open_worker.finished.connect(self.open_thread.quit)
        self.open_worker.finished.connect(self.open_worker.deleteLater)
        self.open_thread.finished.connect(self.open_thread.deleteLater)
        self.open_thread.start()


    def onPortOpened(self, ser, mode): 
        self.ser = ser
        self.serial_opened = True
        if mode == "r":
            self.start_receiver = True 
        
        elif mode == "t": 
            self.start_transmitter = True 
        
        if not getattr(self, "_timer_connected", False): 
            self.timer.timeout.connect(self.updateData)
            self._timer_connected = True
            
        if not self.timer.isActive(): 
            self.timer.start(500)
        
        QMessageBox.information( self, "Success", f"Port {self.arduino_port} opened at {self.baud} baud." )
        
    
    def onPortOpenError(self, error_msg): 
        QMessageBox.critical(self, "Error", f"Failed to open port: {error_msg}")


    def setPortSettings(self, r_or_t):
        if r_or_t == "r":
            self.r_port_window = PortSettingWindow(self)
            self.r_port_window.show()
        else:
            self.t_port_window = PortSettingWindow(self)
            self.t_port_window.show()




