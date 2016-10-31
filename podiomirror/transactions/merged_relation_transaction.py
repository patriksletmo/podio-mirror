from podiomirror.transactions.transaction import Transaction, MODIFY_RELATION


class MergedRelationTransaction(Transaction):
    def __init__(self, app_id=None, field_id=None, parent_id=None):
        super().__init__(MODIFY_RELATION)

        self.app_id = app_id
        self.field_id = field_id
        self.parent_id = parent_id
        self.add_children = []
        self.remove_children = []

    def add_child(self, child):
        if child in self.remove_children:
            self.remove_children.remove(child)

        self.add_children.append(child)

    def remove_child(self, child):
        if child in self.add_children:
            self.add_children.remove(child)

        self.remove_children.append(child)

    def serialize(self):
        raise RuntimeError()

    def deserialize(self, json_data):
        raise RuntimeError()
