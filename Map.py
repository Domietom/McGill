from PySide6.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
from PySide6.QtCore import QPoint, Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QWheelEvent, QPalette, QPixmap
from CoordConverter import utm_to_screen, screen_to_utm, utm_to_geo, zoom_point, inv_zoom_point, geo_to_utm
import xml.etree.ElementTree as ET
from Aircraft import Aircraft

class Map(QWidget):

    def __init__(self, apt, xml_class, scenario):
        super().__init__()

        self.setStyleSheet("background: lightgrey;")

        self.center = self.rect().center()
        self.airport = apt
        self.scenario = scenario
        self.zoom = 0.1
        self.offset = QPointF()

        self.last_pos = QPointF(0,0)

        self.conflicts = []

        self.xml_class = xml_class

        self.waitingForConflictPoint = False
        self.waitingForTrajectoryPoints = False

        self.trajectory = []
        self.allAircraft = []
        self.currentAircraft = Aircraft()
    
    def get_screen_size(self):
        return self.width(), self.height()

    def paintEvent(self, event):

        painter = QPainter(self)
        pen = QPen(Qt.darkBlue)
        pen.setWidth(10)
        painter.setPen(pen)

        for runway in self.airport.runways :
            ext1 = utm_to_screen(runway.side1[1], self.zoom, self.offset, self.airport.center, self.get_screen_size())
            ext1 = QPointF(ext1[0],ext1[1])
            ext2 = utm_to_screen(runway.side2[1], self.zoom, self.offset, self.airport.center, self.get_screen_size())
            ext2 = QPointF(ext2[0], ext2[1])

            painter.drawLine(ext1, ext2)
        
        pen.setWidth(2)
        painter.setPen(pen)

        # for taxiNode in self.airport.taxiNodes.values() :
        #     node = utm_to_screen(taxiNode.pos, self.zoom, self.airport.center, self.get_screen_size())
        #     node = QPoint(node[0], node[1])
        #     painter.drawPoint(node)

        for taxiSegment in self.airport.taxiSegments :
            ext1 = utm_to_screen(taxiSegment.node1.pos, self.zoom, self.offset, self.airport.center, self.get_screen_size())
            ext1 = QPointF(ext1[0],ext1[1])
            ext2 = utm_to_screen(taxiSegment.node2.pos, self.zoom, self.offset, self.airport.center, self.get_screen_size())
            ext2 = QPointF(ext2[0], ext2[1])

            painter.drawLine(ext1, ext2)

        pen = QPen(Qt.red)
        pen.setWidth(10)
        painter.setPen(pen)

        for conflict in self.conflicts :
            delta = zoom_point(conflict, self.zoom, self.offset, self.get_screen_size())
            painter.drawEllipse(delta, 3, 3)

        trajectories_dico = list(self.read_trajectories().values())

        pen.setWidth(4)
        painter.setPen(pen)
        
        for trajectory in trajectories_dico:
            tj_1 = trajectory[0]

            ext1_geo = (tj_1[0], tj_1[1])
            ext1_utm = geo_to_utm(ext1_geo[0], ext1_geo[1])
            ext1_screen = utm_to_screen(ext1_utm, self.zoom, self.offset, self.airport.center, self.get_screen_size())
            ext1 = QPointF(ext1_screen[0],ext1_screen[1])
            tj_1 = ext1

            for point in trajectory[1:]:

                ext2_geo = (point[0], point[1])
                ext2_utm = geo_to_utm(ext2_geo[0], ext2_geo[1])
                ext2_screen = utm_to_screen(ext2_utm, self.zoom, self.offset, self.airport.center, self.get_screen_size())
                ext2 = QPointF(ext2_screen[0], ext2_screen[1])
                painter.drawLine(ext1, ext2)

                ext1 = ext2

            icon = QPixmap(r"images\user_position.jpg")
            iconSize = 30
            painter.drawPixmap(tj_1.x()-iconSize/2, tj_1.y()-iconSize/2, iconSize, iconSize, icon)

        pen = QPen(Qt.black)
        pen.setWidth(6)
        painter.setPen(pen)

        if len(self.trajectory)>=2:
            start = self.trajectory[0]
            ext1 = zoom_point(start, self.zoom, self.offset, self.get_screen_size())

            for point in self.trajectory[1:]:

                ext2 = zoom_point(point, self.zoom, self.offset, self.get_screen_size())
                painter.drawLine(ext1, ext2)

                ext1 = ext2

        for aircraft in self.allAircraft:
            trajectory = aircraft.trajectory

            if aircraft == self.currentAircraft:
                pen = QPen(Qt.darkYellow)
                pen.setWidth(6)
                painter.setPen(pen)

            else :
                pen = QPen(Qt.black)
                pen.setWidth(6)
                painter.setPen(pen)

            if len(trajectory)>=2:
                start = trajectory[0]
                ext1 = zoom_point(start, self.zoom, self.offset, self.get_screen_size())

                for point in trajectory[1:]:

                    ext2 = zoom_point(point, self.zoom, self.offset, self.get_screen_size())
                    painter.drawLine(ext1, ext2)

                    ext1 = ext2


        painter.end()

    def wheelEvent(self, event: QWheelEvent):
        
        delta = event.angleDelta().y()

        if delta > 0:
            self.zoom *= 1.1
        else:
            self.zoom *= 0.9

        self.zoom = max(0.01, min(self.zoom, 10))

        # delta = screen_to_utm(event.position(), self.zoom, self.offset, self.center, self.get_screen_size()) - mouse_pos
        # delta = (delta.x(), delta.y())
        # zoom_offset = utm_to_screen(delta, self.zoom, self.offset, self.center, self.get_screen_size())

        # self.offset += QPointF(zoom_offset[0], zoom_offset[1])
        self.update()

    def mousePressEvent(self, event):

        if event.button() == Qt.RightButton:

            if self.waitingForConflictPoint:
                screen_pos = event.pos()
                delta = inv_zoom_point(screen_pos, self.zoom, self.offset, self.get_screen_size())
                self.conflicts.append(delta)
                self.update()

                utm_pos = screen_to_utm(screen_pos, self.zoom, self.offset, self.airport.center, self.get_screen_size())
                geo_pos = utm_to_geo(utm_pos.x(), utm_pos.y(), self.airport.zoneNumber, self.airport.zoneLetter)

                # offset, ok = QInputDialog.getInt(self, "Entrée","Entrez un entier :", value=0)
                # if ok :
                #     self.xml_class.intersection_type(geo_pos, offset)
                #     self.xml_class.write()
                # else :
                #     self.conflicts = self.conflicts[:-1]

                self.edit = QLineEdit(self)
                self.edit.setGeometry(event.x(), event.y(), 40, 25)
                self.edit.setToolTip("Please enter the offset in meters")
                self.edit.show()
                self.edit.setFocus()
                self.edit.returnPressed.connect(lambda: self.valider(geo_pos))

                self.waitingForConflictPoint = False
            
            if self.waitingForTrajectoryPoints:
                screen_pos = event.pos()
                delta = inv_zoom_point(screen_pos, self.zoom, self.offset, self.get_screen_size())
                self.trajectory.append(delta)
                self.update()

        if event.button() == Qt.LeftButton:

            self.last_pos = event.pos()

    def valider(self, geo_pos):
        xml_offset = int(self.edit.text())
        self.xml_class.intersection_type(geo_pos, xml_offset)

        self.edit.hide()
        self.edit.deleteLater()

    def mouseMoveEvent(self, event):

        if event.buttons() & Qt.LeftButton:
            delta = event.pos() - self.last_pos
            self.offset += delta
            self.last_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        pass

    def read_trajectories(self):
        trajectories_dico = {}
        tree = ET.parse(self.scenario)
        root = tree.getroot()

        for trajectory in root.findall('trajectory'):
            
            # Get aircraft ID
            ac_id = int(trajectory.get('ac-id'))
            trajectories_dico[ac_id] = []
            
            # Analyze waypoints the aircraft will have to go to
            waypoints = trajectory.find('waypoints')
            
            # Go through every waypoint coordinates and store them in the local list
            if waypoints is not None:
                for waypoint in waypoints.findall('waypoint'):
                    lat = float(waypoint.get('lat'))
                    lon = float(waypoint.get('lon'))
                    speed = float(waypoint.get('speed')) #* 0.5144 #Conversion noeuds -> m/s
                    trajectories_dico[ac_id].append([lat, lon, speed])
        return trajectories_dico


# https://www.w3schools.com/python/trypython.asp?filename=demo_ref_string_split2