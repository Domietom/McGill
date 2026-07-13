from PySide6.QtWidgets import (QFrame, QLabel, QPushButton, QVBoxLayout, QHBoxLayout)
from PySide6.QtCore import Qt

class AircraftItem(QFrame):

    def __init__(self, aircraftId):
        super().__init__()

        self.setFrameShape(QFrame.Box)
        self.setLineWidth(2)

        title = QLabel(f"Aircraft {aircraftId}")
        title.setStyleSheet("font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        deleteButton = QPushButton("Delete")
        conflictButton = QPushButton("Add conflict")

        buttons = QHBoxLayout()
        buttons.addWidget(deleteButton)
        buttons.addWidget(conflictButton)

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addLayout(buttons)

        # self.setStyleSheet("""QFrame {
        #                         background-color: white;
        #                         border: 2px solid #999;
        #                         border-radius: 8px;}

        #                     QPushButton {
        #                         padding: 4px;}

        #                     QLabel {
        #                         font-size: 12pt;
        #                         font-weight: bold;}
        #                     """)
