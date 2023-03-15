import json
import csv
from xml.etree.ElementTree import Element, SubElement, tostring
from abc import ABC, abstractmethod

class Exporter(ABC):
    @abstractmethod
    def export(self, data):
        pass

class JsonExporter(Exporter):
    def export(self, data):
        return json.dumps(data)


class CsvExporter(Exporter):
    def export(self, data):
        output = []
        writer = csv.writer(output)
        for row in data:
            writer.writerow(row)
        return '\n'.join(output)


class XmlExporter(Exporter):
    def export(self, data):
        root = Element('data')
        for row in data:
            row_element = SubElement(root, 'row')
            for key, value in row.items():
                cell_element = SubElement(row_element, key)
                cell_element.text = str(value)
        return tostring(root).decode('utf-8')

class ExporterFactory:
    @staticmethod
    def create_exporter(export_type):
        if export_type == 'json':
            return JsonExporter()
        elif export_type == 'csv':
            return CsvExporter()
        elif export_type == 'xml':
            return XmlExporter()
        else:
            raise ValueError(f'Unknown export type: {export_type}')
