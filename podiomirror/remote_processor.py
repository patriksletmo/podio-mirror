from podiomirror.transaction_processor import TransactionProcessor
from podiomirror.transactions.noop_transaction import NoOpTransaction
from podiomirror.transactions.transaction import ADD_ITEM, MODIFY_ITEM, \
    DELETE_ITEM, MODIFY_RELATION
from podiomirror.transport import call_authenticated_endpoint, POST, PUT, DELETE, \
    GET


class RemoteProcessor(TransactionProcessor):
    def __init__(self, tokens=None):
        self.tokens = tokens
        self.id_mappings = {}

    def using_tokens(self, tokens):
        return RemoteProcessor(tokens)

    def begin_processing(self, transactions):
        self.id_mappings = {}

    def process_transaction(self, transaction):
        if type(transaction) is NoOpTransaction:
            return

        token = self.tokens[transaction.app_id].get_valid_token()
        if transaction.transaction_type == ADD_ITEM:
            endpoint = '/item/app/{}/'.format(transaction.app_id)
            parameters = {
                'fields': transaction.item_data
            }
            response = call_authenticated_endpoint(token, endpoint, POST, parameters).json()
            new_item_id = response['item_id']
            self.id_mappings[transaction.item_id] = new_item_id
            transaction.item_id = new_item_id
        elif transaction.transaction_type == MODIFY_ITEM:
            transaction.item_id = self.podio_id(transaction.item_id)
            endpoint = '/item/{}'.format(transaction.item_id)
            parameters = {
                'fields': transaction.item_data['fields']
            }
            call_authenticated_endpoint(token, endpoint, PUT, parameters)
        elif transaction.transaction_type == DELETE_ITEM:
            transaction.item_id = self.podio_id(transaction.item_id)
            endpoint = '/item/{}'.format(transaction.item_id)
            call_authenticated_endpoint(token, endpoint, DELETE)
        elif transaction.transaction_type == MODIFY_RELATION:
            endpoint = '/item/{}'.format(transaction.parent_id)
            response = call_authenticated_endpoint(token, endpoint, GET).json()
            current_relations_field = RemoteProcessor.find_field(response, transaction.field_id)
            new_relations = []
            if current_relations_field is not None:
                current_relations = [x['value']['item_id'] for x in current_relations_field['values']]
                new_relations.extend(current_relations)

            for added_relation in transaction.add_children:
                relation = self.podio_id(added_relation)
                if relation not in new_relations:
                    new_relations.append(relation)

            for removed_relation in transaction.remove_children:
                relation = self.podio_id(removed_relation)
                if relation in new_relations:
                    new_relations.remove(relation)

            parameters = {
                'fields': [
                    {
                        'external_id': transaction.field_id,
                        'values': new_relations
                    }
                ]
            }
            call_authenticated_endpoint(token, endpoint, PUT, parameters)

    def podio_id(self, transaction_id):
        if transaction_id in self.id_mappings:
            return self.id_mappings[transaction_id]
        else:
            return transaction_id

    @staticmethod
    def find_field(data, field_id):
        for field in data['fields']:
            if field['external_id'] == field_id:
                return field

        return None
