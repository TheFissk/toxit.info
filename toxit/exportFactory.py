import csv
import json
from io import StringIO, BytesIO
from xml.etree.ElementTree import Element, SubElement, tostring

from django.http import HttpResponse, FileResponse


class Exporter:
    def __init__(self, data):
        self.exportData = data

    def export(self):
        raise NotImplementedError


class JsonExporter(Exporter):
    def export(self):
        data = json.dumps(self.exportData, indent=2)
        bytes = BytesIO(data.encode('utf-8'))
        return FileResponse(bytes)


class CsvExporter(Exporter):
    def export(self):
        # setup the csv writer
        csv_file = StringIO()
        writer = csv.DictWriter(
            csv_file, fieldnames=self.exportData['sub_nodes_context'][0].keys())
        # write the nodes header
        writer.writeheader()
        # write the nodes data
        writer.writerows(self.exportData['sub_nodes_context'])
        # reintialize the writer, but with the edges fieldnames
        # check to see if there are any mod edges
        try:
            writer = csv.DictWriter(
                csv_file, fieldnames=self.exportData['mod_edges_context'][0].keys())
        except IndexError:
            pass
        else:
            writer.writeheader()
            writer.writerows(self.exportData['mod_edges_context'])
        try:
            writer = csv.DictWriter(
                csv_file, fieldnames=self.exportData['author_edges_context'][0].keys())
        except IndexError:
            pass
        else:
            writer.writeheader()
            writer.writerows(self.exportData['author_edges_context'])

        # Return CSV file as a response
        # response = HttpResponse(csv_file.getvalue(), content_type='text/csv')
        # response['Content-Disposition'] = 'attachment; filename="export.csv"'
        return FileResponse(csv_file)


class XmlExporter(Exporter):
    def export(self):
        # Create root XML element
        root = Element('root')

        # Add data as child elements
        for key, values in self.exportData.items():
            for value in values:
                child = SubElement(root, 'data')
                for col in key:
                    SubElement(child, col).text = str(value.get(col, ''))

        # Write XML to a BytesIO object
        data = tostring(root, encoding='utf-8')
        return BytesIO(data)


class ExporterFactory:
    def create_exporter(self, file_type, data):
        if file_type == 'json':
            return JsonExporter(data)
        elif file_type == 'csv':
            return CsvExporter(data)
        elif file_type == 'xml':
            return XmlExporter(data)
        else:
            raise ValueError(f'Invalid file type: {file_type}')
