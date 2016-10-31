from abc import ABC, abstractmethod


ADD_ITEM = 'add_item'
MODIFY_ITEM = 'modify_item'
DELETE_ITEM = 'delete_item'
ADD_RELATION = 'add_relation'
MODIFY_RELATION = 'modify_relation'
REMOVE_RELATION = 'remove_relation'
NOOP_TRANSACTION = 'noop'


class Transaction(ABC):
    def __init__(self, transaction_type):
        self.storage_id = None
        self.transaction_type = transaction_type
        self.child_transactions = []

    @abstractmethod
    def serialize(self):
        pass

    @abstractmethod
    def deserialize(self, json_data):
        pass

    def mark_resolved_remotely(self, transaction_storage):
        if self.storage_id is not None:
            transaction_storage.mark_resolved_remotely(self.storage_id)

        for transaction in self.child_transactions:
            transaction_storage.mark_resolved_remotely(transaction.storage_id)
