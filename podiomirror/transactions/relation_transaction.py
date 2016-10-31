import json

from PodioMirror.src.transactions.transaction import Transaction


class RelationTransaction(Transaction):
    def __init__(self, transaction_type, app_id=None, field_id=None, parent_id=None, child_id=None):
        super().__init__(transaction_type)

        self.app_id = app_id
        self.field_id = field_id
        self.parent_id = parent_id
        self.child_id = child_id

    def serialize(self):
        return json.dumps({
            'app_id': self.app_id,
            'field_id': self.field_id,
            'parent': self.parent_id,
            'child': self.child_id
        })

    def deserialize(self, json_data):
        data = json.loads(json_data)

        self.app_id = data['app_id']
        self.field_id = data['field_id']
        self.parent_id = data['parent']
        self.child_id = data['child']
