
class Select:
    def __init__(self):
        self.app_id = None
        self.where_clauses = []

    def from_app(self, app_id):
        self.app_id = app_id

        return self

    def where(self, *args):
        self.where_clauses.extend(args)

        return self
