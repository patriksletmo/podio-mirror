from abc import ABC, abstractmethod


class TransactionStorage(ABC):
    @abstractmethod
    def store_transaction(self, transaction):
        pass

    @abstractmethod
    def mark_resolved_locally(self, transaction_id):
        pass

    @abstractmethod
    def mark_resolved_remotely(self, transaction_id):
        pass

    @abstractmethod
    def stored_transactions(self):
        pass
