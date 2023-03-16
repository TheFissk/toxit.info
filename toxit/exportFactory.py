import csv
import json
import pickle
from io import StringIO, BytesIO
from abc import abstractmethod

from django.http import HttpResponse, FileResponse

'''
    Module descripton
'''

class Exporter:
    '''
        Abstract description 
    '''
    @abstractmethod
    def __init__(self, data):
        self.exportData = data

    @abstractmethod
    def export(self):
        raise NotImplementedError
    

class ExporterFactory:
    '''
        description 
    '''
    def create_exporter(self, file_type, data):
        if file_type == 'json':
            return JsonExporter(data)
        elif file_type == 'csv':
            return CsvExporter(data)
        elif file_type == 'pic':
            return PickleExporter(data)
        else:
            raise ValueError(f'Invalid file type: {file_type}')


class JsonExporter(Exporter):
    '''
        description 
    '''
    def export(self):
        data = json.dumps(self.exportData, indent=2)
        bytes = BytesIO(data.encode('utf-8'))
        return FileResponse(bytes)


class CsvExporter(Exporter):
    '''
        description 
    '''
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
        response = HttpResponse(csv_file.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        return response


class PickleExporter(Exporter):
    '''
        description 
    '''
    def export(self):
        data = pickle.dumps(self.exportData)
        bytes = BytesIO(data)
        return FileResponse(bytes)