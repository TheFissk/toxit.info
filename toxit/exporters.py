from abc import ABC, abstractmethod

class Exporter(ABC):
    @abstractmethod
    def export(self, data):
        pass

class JsonExporter(Exporter):
    def export(self, data):
        # TODO: Implement JSON export logic here
        pass

class CsvExporter(Exporter):
    def export(self, data):
        # TODO: Implement CSV export logic here
        pass

class XmlExporter(Exporter):
    def export(self, data):
        # TODO: Implement XML export logic here
        pass
