from podiomirror.query import Select
from podiomirror.remote_data_store import RemoteDataStore
from podiomirror.transactions.merged_relation_transaction import \
    MergedRelationTransaction
from podiomirror.transactions.noop_transaction import NoOpTransaction
from podiomirror.transactions.transaction import ADD_RELATION, REMOVE_RELATION, \
    ADD_ITEM, DELETE_ITEM, MODIFY_ITEM, MODIFY_RELATION

instance = None


class PodioMirror:
    def __init__(self):
        global instance

        self.authenticator = None
        self.storage = None
        self.local_processor = None
        self.remote_processor = None
        self.local_data_store = None
        self.sync_error_handler = None

        self.remote_data_store = RemoteDataStore()
        self.app_tokens = {}
        self.apps = {}

        instance = self

    @staticmethod
    def instance():
        return instance

    def add_app(self, app_id, app_token):
        self.apps[app_id] = app_token

    def perform_transaction(self, transaction):
        self.local_processor.process_transaction(transaction)
        transaction_id = self.storage.store_transaction(transaction)
        self.storage.mark_resolved_locally(transaction_id)

        return transaction_id

    def execute(self, query):
        return self.local_data_store.execute(query)

    def find_app(self, app_id):
        return self.local_data_store.find_app(app_id)

    def synchronize(self):
        # Upload changed data
        transactions = self.merged_transactions()

        tokens = {}
        for transaction in transactions:
            if type(transaction) is NoOpTransaction:
                continue
            if transaction.app_id not in tokens:
                tokens[transaction.app_id] = self.app_token(transaction.app_id)

        resolved_transactions = self.remote_processor.using_tokens(tokens)\
            .process_transactions(transactions)
        for transaction in resolved_transactions:
            transaction.mark_resolved_remotely(self.storage)

        if len(resolved_transactions) != len(transactions):
            num_failed = len(transactions) - len(resolved_transactions)
            error_message = 'There were {} unresolved transactions and the latest synchronization was aborted'.format(num_failed)
            if self.sync_error_handler is None:
                print(error_message)
            else:
                self.sync_error_handler(error_message)

            return

        # Fetch current data
        for app_id in self.apps.keys():
            token = self.app_token(app_id)
            remote_store = self.remote_data_store.using_token(token)
            app = remote_store.find_app(app_id)
            self.local_data_store.store_app(app)

            items = remote_store.execute(Select().from_app(app_id))
            self.local_data_store.clear_cache(app_id)
            for item in items:
                self.local_data_store.store_item(app_id, item)

    def merged_transactions(self):
        transactions = self.storage.stored_transactions()
        merged = []
        for transaction in transactions:
            if transaction.transaction_type == ADD_RELATION or transaction.transaction_type == REMOVE_RELATION:
                merged_transaction = self.find_merged_transaction(merged, transaction)
                if merged_transaction is None:
                    merged_transaction = MergedRelationTransaction(transaction.app_id, transaction.field_id, transaction.parent_id)
                    merged.append(merged_transaction)

                if transaction.transaction_type == ADD_RELATION:
                    merged_transaction.add_child(transaction.child_id)
                elif transaction.transaction_type == REMOVE_RELATION:
                    merged_transaction.remove_child(transaction.child_id)

                merged_transaction.child_transactions.append(transaction)
            elif transaction.transaction_type == ADD_ITEM or transaction.transaction_type == DELETE_ITEM:
                merged_transaction = self.find_merged_transaction(merged, transaction)
                if merged_transaction is not None:
                    merged.remove(merged_transaction)
                    new_merged_transaction = NoOpTransaction()
                    new_merged_transaction.child_transactions.append(merged_transaction)
                    new_merged_transaction.child_transactions.append(transaction)

                    merged.append(new_merged_transaction)
                else:
                    merged.append(transaction)
            elif transaction.transaction_type == MODIFY_ITEM:
                merged_transaction = self.find_merged_transaction(merged, transaction)
                if merged_transaction is not None:
                    if merged_transaction.transaction_type == DELETE_ITEM:
                        merged_transaction.child_transactions.append(transaction)
                    elif merged_transaction.transaction_type == MODIFY_ITEM:
                        merged_transaction.item_data['fields'].update(transaction.item_data['fields'])
                        if 'new_files' in transaction.item_data:
                            merged_transaction.item_data['new_files'] = transaction.item_data['new_files']
                        merged_transaction.child_transactions.append(transaction)
                else:
                    merged.append(transaction)
            else:
                merged.append(transaction)

        return merged

    def find_merged_transaction(self, merged, new):
        if new.transaction_type == ADD_RELATION or new.transaction_type == REMOVE_RELATION:
            for transaction in merged:
                if transaction.transaction_type == MODIFY_RELATION:
                    if transaction.app_id == new.app_id and \
                       transaction.field_id == new.field_id and \
                       transaction.parent_id == new.parent_id:
                        return transaction
        if new.transaction_type == ADD_ITEM:
            for transaction in merged:
                if (transaction.transaction_type == DELETE_ITEM or
                    transaction.transaction_type == ADD_ITEM) and \
                   transaction.app_id == new.app_id and \
                   transaction.item_id == new.item_id:
                    return transaction
        if new.transaction_type == MODIFY_ITEM:
            for transaction in merged:
                if (transaction.transaction_type == DELETE_ITEM or
                    transaction.transaction_type == MODIFY_ITEM) and \
                   transaction.app_id == new.app_id and \
                   transaction.item_id == new.item_id:
                    return transaction
        if new.transaction_type == DELETE_ITEM:
            for transaction in merged:
                if transaction.transaction_type == ADD_ITEM and \
                                transaction.app_id == new.app_id and \
                                transaction.item_id == new.item_id:
                    return transaction

        return None

    def app_token(self, app_id):
        if app_id not in self.app_tokens:
            self.app_tokens[app_id] = self.authenticator.authenticate_for_app(app_id, self.apps[app_id])

        return self.app_tokens[app_id]
