from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PySide6.QtCore import Qt, Signal

class AircraftItem(QFrame):

    deleteRequested = Signal(QWidget)
    conflictRequested = Signal(QWidget)

    def __init__(self, aircraft):
        super().__init__()

        self.aircraft = aircraft

        self.setFrameShape(QFrame.Box)
        self.setLineWidth(2)

        title = QLabel(f"Aircraft {self.aircraft.ID}")
        title.setStyleSheet("font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.deleteButton = QPushButton("Delete")
        self.conflictButton = QPushButton("Add conflict")

        self.deleteButton.clicked.connect(self.ask_delete)
        self.conflictButton.clicked.connect(self.ask_conflict)

        buttons = QHBoxLayout()
        buttons.addWidget(self.deleteButton)
        buttons.addWidget(self.conflictButton)

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

    def ask_delete(self):
        self.deleteRequested.emit(self)

    def ask_conflict(self):
        self.conflictRequested.emit(self)

    def __repr__(self):
        return f'Aircraft Item {self.aircraft.ID}'
