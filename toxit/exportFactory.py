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
        return data.content.decode('utf-8')


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
    def create_exporter(self, file_type):
        if file_type == 'json':
            return save('rb')