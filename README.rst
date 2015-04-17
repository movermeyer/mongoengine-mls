MultiLingualField for MongoEngine (for Python 2k and 3k)
========================================================

.. image:: https://travis-ci.org/rembish/mongoengine-mls.svg?branch=master
    :target: https://travis-ci.org/rembish/mongoengine-mls

.. image:: https://coveralls.io/repos/rembish/mongoengine-mls/badge.svg
    :target: https://coveralls.io/r/rembish/mongoengine-mls

.. image:: https://pypip.in/download/mongoengine-mls/badge.svg
    :target: https://pypi.python.org/pypi/mongoengine-mls

.. image:: https://pypip.in/version/mongoengine-mls/badge.svg
    :target: https://pypi.python.org/pypi/mongoengine-mls

.. image:: https://pypip.in/py_versions/mongoengine-mls/badge.svg
    :target: https://pypi.python.org/pypi/mongoengine-mls

.. image:: https://pypip.in/implementation/mongoengine-mls/badge.svg
    :target: https://pypi.python.org/pypi/mongoengine-mls

.. image:: https://pypip.in/status/mongoengine-mls/badge.svg
    :target: https://pypi.python.org/pypi/mongoengine-mls

.. image:: https://pypip.in/wheel/mongoengine-mls/badge.svg
    :target: https://pypi.python.org/pypi/mongoengine-mls

.. image:: https://pypip.in/egg/mongoengine-mls/badge.svg
    :target: https://pypi.python.org/pypi/mongoengine-mls

.. image:: https://pypip.in/format/mongoengine-mls/badge.svg
    :target: https://pypi.python.org/pypi/mongoengine-mls

.. image:: https://pypip.in/license/mongoengine-mls/badge.svg
    :target: https://pypi.python.org/pypi/mongoengine-mls

Simple extension for MongoEngine, which adds MultiLingualField (based on
MultiLingualString). Some self-describing examples:

.. code-block:: python

    from locale import setlocale, LC_ALL
    from mongoengine import Document, connect
    from mongoengine_mls import MultiLingualField

    class Country(Document):
        meta = {"indexes": ["name.language"]}
        name = MultiLingualField(required=True)

    setlocale(LC_ALL, "en_US.UTF-8")
    connect("test")

    ru = Country(name={"en": "Russia", "ru": u"Россия"})
    ru.save()

    print(ru.name)  # => Russia
    print(ru.name >> "ru")  # => Россия

    ru2 = Country.objects.first()
    ru2.name = [
        {"language": "en", "value": "Russian Federation"},
        {"language": "ru", "value": u"Российская Федерация"}
    ]
    ru2.save()

    print(ru2.name)  # => Russia Federation
    print(type(ru2.name))  # => <class 'mls.MultiLingualString'>
