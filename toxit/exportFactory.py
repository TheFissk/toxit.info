import csv
import json
import pickle
from io import StringIO, BytesIO
from abc import abstractmethod

from django.http import HttpResponse, FileResponse

'''
    Define the Factory used in our program as per the project requirements
'''


class Exporter:
    '''
        Abstract Exporter definition
    '''

    def __init__(self, data):  # Abstract initializer method that sets the data to be exported
        self.exportData = data

    @abstractmethod
    def export(self):  # Abstract method to export the data in a particular format
        raise NotImplementedError


class ExporterFactory:
    '''
        A factory class to create instances of different Exporter subclasses 
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
        Defines the JSON exporter
    '''

    def export(self):
        # convert the data to JSON
        data = json.dumps(self.exportData, indent=2)
        bytes = BytesIO(data.encode('utf-8'))  # serialize the JSON
        return FileResponse(bytes)  # return as a FileResponse


class CsvExporter(Exporter):
    '''
        Defines the csv exporter
    '''

    def export(self):
        # setup the csv writer
        csv_file = StringIO()  # use a StringIO to serialize the csv
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
        except IndexError:  # no mod edges so we continue on to the author edges
            pass
        else:
            writer.writeheader()
            writer.writerows(self.exportData['mod_edges_context'])
        try:
            writer = csv.DictWriter(
                csv_file, fieldnames=self.exportData['author_edges_context'][0].keys())
        except IndexError:  # no author edges so we continue to export
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
        Defines the pickle exporter 
    '''

    def export(self):
        data = pickle.dumps(self.exportData) # convert the data to Pickle
        bytes = BytesIO(data) # serialize into bytes
        return FileResponse(bytes) #output as File Response
