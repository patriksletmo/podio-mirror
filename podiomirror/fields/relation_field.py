from podiomirror.fields.field import Field


class RelationField(Field):
    @property
    def filter_value(self):
        return self.value
