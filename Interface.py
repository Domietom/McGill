from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QLabel, QPushButton
from Map import Map

class Interface(QWidget):

    def __init__(self, apt, xml_class, scenario):
        super().__init__()

        self.setWindowTitle("Experiment configuration")
        self.showMaximized()

        self.mapWidget = Map(apt, xml_class, scenario)
        self.aircraftList = QListWidget()
        self.aircraftId = 1

        rightPanel = QVBoxLayout()
        rightPanel.addWidget(QLabel("Aircraft list"))
        rightPanel.addWidget(self.aircraftList)

        self.addPlaneButton = QPushButton('+')
        self.addPlaneButton.clicked.connect(self.add_plane)
        rightPanel.addWidget(self.addPlaneButton)

        layout = QHBoxLayout(self)
        layout.addWidget(self.mapWidget, 4)
        layout.addLayout(rightPanel, 1)

    def add_plane(self):
        self.aircraftList.addItem(f"AC{self.aircraftId}")
        self.aircraftId += 1