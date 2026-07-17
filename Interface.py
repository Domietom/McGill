from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QLabel, QPushButton, QListWidgetItem
from PySide6.QtCore import Signal
from PySide6.QtGui import QCloseEvent
from Map import Map
from AircraftItem import AircraftItem
from Aircraft import Aircraft

class Interface(QWidget):

    endTrajectorySignal = Signal(QWidget)

    def __init__(self, apt, xml_class, scenario):
        super().__init__()

        self.setWindowTitle("Experiment configuration")
        self.showMaximized()

        self.mapWidget = Map(apt, xml_class, scenario)
        self.aircraftList = QListWidget()
        self.aircraftList.currentItemChanged.connect(self.on_list_selection)

        self.aircraftId = 1

        rightPanel = QVBoxLayout()
        rightPanel.addWidget(QLabel("Aircraft list"))
        rightPanel.addWidget(self.aircraftList)

        self.endTrajectoryButton = QPushButton('OK')
        self.endTrajectoryButton.setCheckable(True)
        self.endTrajectoryButton.setStyleSheet("""QPushButton:checked {
                                        background-color: yellow;
                                        border: 2px solid black;}""")
        self.endTrajectoryButton.clicked.connect(self.end_trajectory)
        rightPanel.addWidget(self.endTrajectoryButton)

        self.addPlaneButton = QPushButton('+')
        self.addPlaneButton.clicked.connect(self.add_plane)
        rightPanel.addWidget(self.addPlaneButton)

        layout = QHBoxLayout(self)
        layout.addWidget(self.mapWidget, 6)
        layout.addLayout(rightPanel, 1)

    def end_trajectory(self):
        self.mapWidget.waitingForTrajectoryPoints = False
        self.updateOKButton()
        self.mapWidget.allAircraft.append(self.mapWidget.currentAircraft)
        self.mapWidget.currentAircraft = Aircraft()
        self.update()

    def add_plane(self):
        if len(self.mapWidget.currentAircraft.trajectory) != 0:
            self.end_trajectory()

        self.mapWidget.currentAircraft = Aircraft(self.aircraftId)

        card = AircraftItem(self.mapWidget.currentAircraft)

        item = QListWidgetItem()
        item.setSizeHint(card.sizeHint())

        self.aircraftList.setCurrentItem(item)

        card.deleteRequested.connect(lambda w=card, i=item: self.remove_plane(i, w))
        card.conflictRequested.connect(lambda w=card, i=item: self.add_conflict(i,w))

        self.aircraftList.addItem(item)
        self.aircraftList.setItemWidget(item, card)
        
        self.aircraftId += 1
        self.mapWidget.waitingForTrajectoryPoints = True
        self.updateOKButton()

    def remove_plane(self, item, card):

        row = self.aircraftList.row(item)
        self.aircraftList.takeItem(row)

        if card.aircraft in self.mapWidget.allAircraft:
            self.mapWidget.allAircraft.remove(card.aircraft)

        self.update()

        card.deleteLater()

    def add_conflict(self, item, card):
        self.mapWidget.waitingForConflictPoint = True
        self.mapWidget.waitingForTrajectoryPoints = False
        self.aircraftList.setCurrentItem(item)

    def on_list_selection(self, current, previous):
        if current:
            currentAircraftItem = self.aircraftList.itemWidget(current)
            self.mapWidget.currentAircraft = currentAircraftItem.aircraft
        self.update()

    def updateOKButton(self):
        self.endTrajectoryButton.setChecked(self.mapWidget.waitingForTrajectoryPoints)

    def closeEvent(self, event: QCloseEvent):
        self.mapWidget.xml_class.write_all(self.mapWidget.allAircraft)