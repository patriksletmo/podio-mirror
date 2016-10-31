from PodioMirror.src.transactions.transaction import Transaction, NOOP_TRANSACTION


class NoOpTransaction(Transaction):
    def __init__(self):
        super().__init__(NOOP_TRANSACTION)

    def serialize(self):
        raise RuntimeError()

    def deserialize(self, json_data):
        raise RuntimeError()
