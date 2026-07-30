from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QLabel, QPushButton, QListWidgetItem
from PySide6.QtCore import Signal
from PySide6.QtGui import QCloseEvent
from Map import Map
from AircraftItem import AircraftItem
from Aircraft import Aircraft

class Interface(QWidget):

    endTrajectorySignal = Signal(QWidget)

    def __init__(self, apt, xml_class):
        super().__init__()

        self.setWindowTitle("Experiment configuration")
        self.showMaximized()

        self.mapWidget = Map(apt, xml_class)
        self.aircraftList = QListWidget()
        self.aircraftList.currentItemChanged.connect(self.on_list_selection)

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

        loadLayout = QHBoxLayout()
        loadButton = QPushButton('Load a file')
        saveButton = QPushButton('Save')
        loadLayout.addWidget(loadButton)
        loadLayout.addWidget(saveButton)
        rightPanel.addLayout(loadLayout)

        layout = QHBoxLayout(self)
        layout.addWidget(self.mapWidget, 6)
        layout.addLayout(rightPanel, 2)

    def end_trajectory(self):
        self.mapWidget.waitingForTrajectoryPoints = False
        self.updateOKButton()

        currentAircraft = self.mapWidget.currentAircraft
        currentAircraftItem = self.getAircraftItem(currentAircraft)

        if currentAircraft not in self.mapWidget.allAircraft and currentAircraft.ID != 0:
            self.mapWidget.allAircraft.append(currentAircraft)
            
            if currentAircraftItem is not None:
                currentAircraftItem.setSpeedChoice()
            
        if currentAircraftItem is not None:
            currentAircraftItem.setSelected(False)
            
        self.setSize()
        self.mapWidget.currentAircraft = Aircraft()
        self.update()

    def add_plane(self):
        if len(self.mapWidget.currentAircraft.trajectory) > 1:
            self.end_trajectory()

        ids = [aircraft.ID for aircraft in self.mapWidget.allAircraft]
        for i in range(1,20):
            if i not in ids:
                firstAvailableId = i
                break

        self.mapWidget.currentAircraft = Aircraft(firstAvailableId)

        card = AircraftItem(self.mapWidget.currentAircraft)

        item = QListWidgetItem()
        item.setSizeHint(card.sizeHint())

        self.aircraftList.setCurrentItem(item)

        card.deleteRequested.connect(lambda w=card, i=item: self.remove_plane(i, w))
        card.intersectionRequested.connect(lambda w=card, i=item: self.add_intersection(i,w))
        card.followRequested.connect(lambda w=card, i=item: self.add_follow(i,w))

        self.aircraftList.addItem(item)
        self.aircraftList.setItemWidget(item, card)

        self.mapWidget.waitingForTrajectoryPoints = True
        self.updateOKButton()

    def remove_plane(self, item, card):
        row = self.aircraftList.row(item)
        self.aircraftList.takeItem(row)

        if self.mapWidget.waitingForTrajectoryPoints:
            self.end_trajectory()
        if card.aircraft in self.mapWidget.allAircraft:
            self.mapWidget.allAircraft.remove(card.aircraft)
        if len(self.mapWidget.allAircraft) <= 1:
            self.mapWidget.currentAircraft = Aircraft() 

        self.update()
        card.deleteLater()

    def add_intersection(self, item, card):
        self.mapWidget.waitingForIntersectionPoint = True
        self.mapWidget.waitingForTrajectoryPoints = False
        self.mapWidget.waitingForFollowPoint = False
        self.aircraftList.setCurrentItem(item)

    def add_follow(self, item, card):
        self.mapWidget.waitingForFollowPoint = True
        self.mapWidget.waitingForTrajectoryPoints = False
        self.mapWidget.waitingForIntersectionPoint = False
        self.aircraftList.setCurrentItem(item)

    def on_list_selection(self, current, previous):
        if previous:
            previousAircraftItem = self.aircraftList.itemWidget(previous)
            previousAircraftItem.setSelected(False)
            print(previousAircraftItem.aircraft)
        if current:
            if len(self.mapWidget.allAircraft) != 0:
                self.end_trajectory()
                currentAircraftItem = self.aircraftList.itemWidget(current)
                self.mapWidget.currentAircraft = currentAircraftItem.aircraft
                currentAircraftItem.setSelected(True)
                print(currentAircraftItem.aircraft)
        self.setSize()
        self.update()


    def updateOKButton(self):
        self.endTrajectoryButton.setChecked(self.mapWidget.waitingForTrajectoryPoints)

    def closeEvent(self, event: QCloseEvent):
        self.mapWidget.xml_class.write_all(self.mapWidget.allAircraft)

    def getAircraftItem(self, aircraft):
        for i in range(self.aircraftList.count()):
            item = self.aircraftList.item(i)
            widget = self.aircraftList.itemWidget(item)

            if widget.aircraft.ID == aircraft.ID:
                return widget

        return None

    def setSize(self):
        for i in range(self.aircraftList.count()):
            item = self.aircraftList.item(i)
            widget = self.aircraftList.itemWidget(item)

            if widget is not None:
                item.setSizeHint(widget.sizeHint())