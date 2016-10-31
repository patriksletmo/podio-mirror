from PodioMirror.data_store import DataStore

from PodioMirror.src.transport import call_authenticated_endpoint, POST, GET

PODIO_REQUEST_ITEM_LIMIT = 500


class RemoteDataStore(DataStore):
    def __init__(self, token=None):
        self.token = token

    def using_token(self, token):
        return RemoteDataStore(token)

    def execute(self, query):
        if self.token is None:
            raise RuntimeError('Remote query must be prefixed with using_token')

        filters = {}
        for clause in query.where_clauses:
            filters[clause.name] = clause.filter_value

        offset = 0
        total = 1
        items = []
        while len(items) < total:
            endpoint = '/item/app/{}/filter/?fields=items.fields(files)'.format(self.token.app_id)
            response = call_authenticated_endpoint(self.token.get_valid_token(), endpoint, POST, {
                'filters': filters,
                'offset': offset,
                'limit': PODIO_REQUEST_ITEM_LIMIT
            })
            response.raise_for_status()

            data = response.json()
            total = data['filtered']
            offset += len(data['items'])
            items.extend(data['items'])

        return items

    def find_app(self, app_id):
        if self.token is None:
            raise RuntimeError('Remote query must be prefixed with using_token')

        endpoint = '/app/{}'.format(self.token.app_id)
        response = call_authenticated_endpoint(self.token.get_valid_token(), endpoint, GET)
        response.raise_for_status()

        return response.json()
