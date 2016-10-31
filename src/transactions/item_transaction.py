import json

from PodioMirror.src.transactions.transaction import Transaction


class ItemTransaction(Transaction):
    def __init__(self, transaction_type, app_id=None, item_data=None):
        super().__init__(transaction_type)

        self.app_id = app_id
        if item_data is None:
            self.item_id = None
        else:
            self.item_id = item_data.get('item_id')
        self.item_data = item_data

    def serialize(self):
        return json.dumps({
            'app_id': self.app_id,
            'item_id': self.item_id,
            'item_data': self.item_data
        })

    def deserialize(self, json_data):
        data = json.loads(json_data)

        self.app_id = data['app_id']
        self.item_id = data['item_id']
        self.item_data = data['item_data']
