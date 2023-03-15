import csv
import json
from io import StringIO, BytesIO
from xml.etree.ElementTree import Element, SubElement, tostring
import zipfile

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
        # response = FileResponse(file, content_type=file.content_type, as_attachment=True, filename=file.filename)
        return FileResponse(bytes, filename="test.json")


class CsvExporter(Exporter):
    def export(self):
        # Flatten data to a 2D list
        flat_data = []
        for key, values in self.exportData.items():
            for value in values:
                row = [value.get(col, '') for col in key]
                flat_data.append(row)

        # Write flattened data to CSV file in memory
        csv_file = StringIO()
        writer = csv.writer(csv_file)
        writer.writerows([key for key in self.exportData.keys()])
        writer.writerows(flat_data)

        # Return CSV file as a response
        response = HttpResponse(csv_file.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        return response


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


# class ZipExporter(Exporter):
#     def export(self):
#         # Create in-memory zip file
#         zip_file = BytesIO()
#         with zipfile.ZipFile(zip_file, mode='w', compression=zipfile.ZIP_DEFLATED) as archive:
#             # Add each file to the archive
#             for file_type, exporter in self.exportData.items():
#                 file = exporter.export()
#                 archive.writestr(f'export.{file_type}', file.getvalue())

#         # Return zip file as a response
#         zip_file.seek(0)
#         response = HttpResponse(zip_file.getvalue(), content_type='application/zip')
#         response['Content-Disposition'] = 'attachment; filename="export.zip"'
#         return response


class ExporterFactory:
    def create_exporter(self, file_type, data):
        if file_type == 'json':
            return JsonExporter(data)
        elif file_type == 'csv':
            return CsvExporter(data)
        elif file_type == 'xml':
            return XmlExporter(data)
        # elif file_type == 'zip':
        #     return ZipExporter({
        #         'json': JsonExporter(self.exportData),
        #         'csv': CsvExporter(self.exportData),
        #         'xml': XmlExporter(self.exportData),
        #     })
        else:
            raise ValueError(f'Invalid file type: {file_type}')