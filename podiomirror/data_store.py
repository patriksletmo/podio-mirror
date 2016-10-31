from abc import ABC, abstractmethod


class DataStore(ABC):
    @abstractmethod
    def execute(self, query):
        pass

    @abstractmethod
    def find_app(self, app_id):
        pass

    def clear_cache(self, app_id):
        # TODO: Move out to new class LocalDataStore?
        raise NotImplementedError()

    def store_item(self, app_id, item):
        # TODO: Move out to new class LocalDataStore?
        raise NotImplementedError()

    def store_app(self, app):
        # TODO: Move out to new class LocalDataStore?
        raise NotImplementedError()

