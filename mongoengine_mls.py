#!/usr/bin/env python
from copy import deepcopy
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentListField, StringField
from mls import mls
from six import string_types

__all__ = ["MultiLingualField"]


class MultiLingualEmbeddedDocument(EmbeddedDocument):
    language = StringField(required=True, min_length=2, max_length=3)
    value = StringField(required=True)


class MultiLingualField(EmbeddedDocumentListField):
    def __init__(self, **kwargs):
        super(MultiLingualField, self).__init__(
            MultiLingualEmbeddedDocument, **kwargs)

    def __set__(self, instance, value):
        if value is None:
            if self.null:
                value = None
            elif self.default is not None:
                value = self.default
                if callable(value):
                    value = value()

        if instance._initialised:
            if self.name not in instance._data \
                    or instance._data[self.name] != value \
                    or type(instance._data[self.name]) != type(value):
                instance._mark_as_changed(self.name)

        instance._data[self.name] = value

    def to_python(self, value):
        if isinstance(value, mls):
            return value

        value = super(MultiLingualField, self).to_python(value)

        return mls(dict(
            (item.language, item.value) for item in value
        ))

    def to_mongo(self, value):
        value = deepcopy(value)
        if isinstance(value, (dict, string_types)):
            value = mls(value)

        if isinstance(value, mls):
            return [
                {"language": key, "value": data}
                for key, data in value._mapping.items()
            ]

        return super(MultiLingualField, self).to_mongo(value)

    def validate(self, value):
        if isinstance(value, (list, tuple, set, frozenset)):
            for item in value:
                if not isinstance(item, dict) \
                        or "language" not in item \
                        or "value" not in item:
                    self.error("MultiLingualField accepts MultiLingualString, "
                               "list of dictionaries, dictionary or "
                               "string/unicode as it's value.")
        elif not isinstance(value, (mls, string_types, dict)):
            super(MultiLingualField, self).validate(value)
