
class Field:
    def __init__(self, name):
        self.name = name
        self.compare = None
        self.value = None

    def is_equal_to(self, value):
        self.compare = 'eq'
        self.value = value

        return self

    @property
    def filter_value(self):
        return self.value
