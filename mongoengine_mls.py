#!/usr/bin/env python
# pylint: disable=W0212,C0103
"""
Unicode-like field for multiple language mutations, which can be used with
MongoEngine package.
"""
from copy import deepcopy
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import ListField, EmbeddedDocumentField, StringField
from mls import mls
from sys import version_info

__all__ = ["MultiLingualField"]

if version_info < (3, 0, 0):
    string_types = basestring
else:
    string_types = str


class MultiLingualEmbeddedDocument(EmbeddedDocument):
    """
    Internal embedded document to store information about language mutations.
    You can simply apply index on any field in your Document, which uses
    MultiLingualField. For example:

        >>> from mongoengine import Document
        >>> from mongoengine_mls import MultiLingualField
        >>> class Country(Document):
        ...     meta = {"indexes": ["name.language"]}
        ...     name = MultiLingualField()
    """
    language = StringField(required=True, min_length=2, max_length=3)
    value = StringField(required=True)


class MultiLingualField(ListField):
    """
    Special field, that will be automatically transformed to MultiLingualString
    after extracting from MongoDB. See `mls` package documentation for more
    advantages and useful tips.
    """
    def __init__(self, **kwargs):
        null = kwargs.pop("null", False)
        super(MultiLingualField, self).__init__(
            field=EmbeddedDocumentField(MultiLingualEmbeddedDocument), **kwargs
        )
        self.null = null

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

        value = deepcopy(value)
        if isinstance(value, (dict, string_types)):
            value = mls(value)
        elif isinstance(value, (list, tuple, set, frozenset)):
            try:
                value = mls(**dict(
                    (item["language"], item["value"]) for item in value
                ))
            except (KeyError, TypeError, ValueError):
                pass

        instance._data[self.name] = value

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return instance._data.get(self.name)

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
