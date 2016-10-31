import traceback
from abc import ABC, abstractmethod


class TransactionProcessor(ABC):
    @abstractmethod
    def process_transaction(self, transaction):
        pass

    def begin_processing(self, transactions):
        pass

    def process_transactions(self, transactions):
        resolved_transactions = []
        try:
            self.begin_processing(transactions)
            for transaction in transactions:
                self.process_transaction(transaction)
                resolved_transactions.append(transaction)
        except Exception:
            traceback.print_exc()

        return resolved_transactions
