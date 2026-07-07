import xml.etree.ElementTree as ET
from xml.dom import minidom

class WriteXML:

    def __init__(self):
        self.root = ET.Element('aircraft')

    def intersection_type(self, pos, offset_value):
        ac4 = ET.SubElement(self.root, 'ac')
        ac4.set('id', '4')
        type4 = ET.SubElement(ac4, 'conflict')
        type4.set('type', 'intersection')
        location = ET.SubElement(type4, 'location')
        location.set('lat', str(pos[0]))
        location.set('lon', str(pos[1]))
        offset = ET.SubElement(type4, 'offset')
        offset.set('dist', str(offset_value))

    def write(self):
        xml_data = ET.tostring(self.root)
        dom = minidom.parseString(xml_data)
        with open("simulation.xml", "w", encoding="utf-8") as xml_file:
            xml_file.write(dom.toprettyxml(indent="  "))
            xml_file.flush()