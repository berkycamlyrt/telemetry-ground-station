from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QMessageBox, QVBoxLayout, QGridLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class PortSettingWindow(QWidget, ):
        def __init__(self, parent_window):
            super().__init__()
            
            self.parent_window = parent_window

            self.initVariables()
            self.setupUi()
            self.centerToParent()

        def initVariables(self):
            self.font = QFont(self.parent_window.font)
            self.font.setPointSize(14)


        def setupUi(self):
            self.setWindowTitle("Port Settings")
            self.resize(480, 270)
            self.setMinimumSize(320, 240)

            self.main_layout = QVBoxLayout(self)
            self.main_layout.setContentsMargins(40, 24, 40, 24)
            self.main_layout.setSpacing(14)

            self.setupForm()
            self.setupButton()


        def setupForm(self):
            self.label_com = QLabel("COM Port")
            self.label_com.setFont(self.font)
            self.label_com.setAlignment(Qt.AlignCenter)

            self.input_com = QLineEdit()
            self.input_com.setFont(self.font)
            self.input_com.setMinimumHeight(36)
            self.input_com.setAlignment(Qt.AlignCenter)

            self.label_baud = QLabel("Baud")
            self.label_baud.setFont(self.font)
            self.label_baud.setAlignment(Qt.AlignCenter)

            self.input_baud = QLineEdit()
            self.input_baud.setFont(self.font)
            self.input_baud.setMinimumHeight(36)
            self.input_baud.setAlignment(Qt.AlignCenter)

            self.main_layout.addStretch()

            self.main_layout.addWidget(self.label_com)
            self.main_layout.addWidget(self.input_com)

            self.main_layout.addSpacing(8)

            self.main_layout.addWidget(self.label_baud)
            self.main_layout.addWidget(self.input_baud)

            self.main_layout.addSpacing(16)


        def setupButton(self):
            self.button_set = QPushButton("Set")
            self.button_set.setFont(self.font)
            self.button_set.setMinimumHeight(48)
            self.button_set.clicked.connect(self.onSetButtonClick)

            self.main_layout.addWidget(self.button_set)
            self.main_layout.addStretch()

        
        def centerToParent(self):
            parent_geo = self.parent_window.frameGeometry()
            center_point = parent_geo.center()

            self_geo = self.frameGeometry()
            self_geo.moveCenter(center_point)
            self.move(self_geo.topLeft())


        def onSetButtonClick(self):
            com_text = self.input_com.text()
            baud_text = self.input_baud.text()
                
            com_len_b = len(com_text) == 4 or len(com_text) == 5
            com_start_b = com_text[:3] == "COM"
            com_end_b = com_text[3:].isdigit()

            baud_list = [300, 600, 750, 1200, 2400, 4800, 9600, 19200, 31250, 38400, 57600, 74880, 115200, 230400, 250000, 460800, 500000, 921600, 1000000, 2000000]
            baud_format_b = baud_text.isdigit()    

            com_error = not (com_len_b and com_start_b and com_end_b)
            baud_error = not (baud_format_b and (int(baud_text) in baud_list))


            if com_error:
                QMessageBox.critical(self, "Error", "Wrong COM Input!")
            
            elif baud_error:
                QMessageBox.critical(self, "Error", "Wrong Baud Input")

            else:
                self.parent_window.baud = int(baud_text)
                self.parent_window.arduino_port = com_text

                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Information)
                msg.setText("Port settings updated successfully!")
                msg.setWindowTitle("Success")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.finished.connect(self.close)  # Close this window after the success message
                msg.show()
