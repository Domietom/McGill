import xml.etree.ElementTree as ET
from xml.dom import minidom

class WriteXML:

    def __init__(self):
        self.conflictsRoot = ET.Element('aircraft')
        self.trajectoriesRoot = ET.Element('trajectories')

    def intersection_type(self, pos, offset_value):
        root = self.conflictsRoot
        ac4 = ET.SubElement(root, 'ac')
        ac4.set('id', '4')
        type4 = ET.SubElement(ac4, 'conflict')
        type4.set('type', 'intersection')
        location = ET.SubElement(type4, 'location')
        location.set('lat', str(pos[0]))
        location.set('lon', str(pos[1]))
        offset = ET.SubElement(type4, 'offset')
        offset.set('dist', str(offset_value))
        self.write(root, "simulation.xml")

    def write(self, root, filename):
        xml_data = ET.tostring(root)
        dom = minidom.parseString(xml_data)
        with open(filename, "w", encoding="utf-8") as xml_file:
            xml_file.write(dom.toprettyxml(indent="  "))
            xml_file.flush()

    def write_trajectory(self, aircraft):
        root = self.trajectoriesRoot
        ac = ET.SubElement(root, 'trajectory')
        ac.set('ac-id', str(aircraft.ID))
        waypoints = ET.SubElement(ac, 'waypoints')
        for point in aircraft.trajectory:
            waypoint = ET.SubElement(waypoints, 'waypoint')
            waypoint.set('lat', str(point.x()))
            waypoint.set('lon', str(point.y()))
            waypoint.set('speed', '5')

        self.write(root, "trajTEST.xml")
