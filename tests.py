# coding=utf-8
from locale import setlocale, LC_ALL
from uuid import uuid4
from mongoengine.errors import ValidationError
from mls import mls
from mongoengine.connection import connect
from mongoengine.document import Document
from mongoengine.fields import StringField
from os import environ
from unittest import TestCase as BaseTestCase

from mongoengine_mls import MultiLingualField


class Country(Document):
    meta = {"collection": uuid4().hex}

    code = StringField(required=True, min_length=2, max_length=2)
    name = MultiLingualField()
    nullable = MultiLingualField(null=True)

    @classmethod
    def by_code(cls, code):
        return cls.objects(code=code).first()

    def __repr__(self):
        return "<%s[%s]>" % (self.__class__.__name__, self.code)


class TestCase(BaseTestCase):
    def setUp(self):
        setlocale(LC_ALL, "en_US.UTF_8")

        connect(
            db=environ.get("TEST_DB", "test"),
            host=environ.get("TEST_HOST", "localhost"),
            port=environ.get("TEST_PORT", 27017),
        )

        Country(
            code="ru", name=mls(ru=u"Россия", en="Russia", cs="Rusko")
        ).save()
        Country(
            code="cz", name=mls(ru=u"Чехия", en="Czech Republic", cs=u"Česko")
        ).save()

    def test_read(self):
        ru = Country.by_code("ru")

        self.assertEqual(ru.code, "ru")
        self.assertEqual(ru.name, "Russia")

    def test_save(self):
        ru = Country.by_code("ru")
        ru.name <<= "Russian Federation"
        ru.save()

        ru2 = Country.by_code("ru")

        self.assertEqual(repr(ru2.name), "en'Russian Federation'")
        self.assertEqual(unicode(ru2.name >> "cs"), u"Rusko")

    def test_rewrite_with_list(self):
        cz = Country.by_code("cz")

        self.assertIsInstance(cz.name, mls)

        cz.name = [
            {"language": "cs", "value": u"Česká republika"},
            {"language": "en", "value": "Czech Republic"},
            {"language": "ru", "value": u"Чешская Республика"},
        ]
        cz.save()

        cz2 = Country.by_code("cz")

        self.assertEqual(unicode(cz2.name >> "ru"), u"Чешская Республика")

    def test_rewrite_with_dict(self):
        ru2 = Country.by_code("ru")
        ru2.name = {
            "ru": u"Российская Федерация",
            "cs": u"Ruská federace",
            "en": "Russian Federation"
        }
        ru2.save()

        ru3 = Country.by_code("ru")

        self.assertEqual(
            unicode(ru3.name.translate_to("cs")), u"Ruská federace")

    def test_remove_other(self):
        cz2 = Country.by_code("cz")
        cz2.name = u"Czech Republic"  # Removing all mutations except en_US
        cz2.save()

        cz3 = Country.by_code("cz")

        self.assertEqual(str(cz3.name), "Czech Republic")
        self.assertEqual(unicode(cz3.name >> "cs"), u"Czech Republic")

    def test_invalids(self):
        xy = Country(code="xy")
        xy.name = ["foo", "bar"]

        self.assertRaises(ValidationError, xy.save)

        xy.name = 123
        self.assertRaises(ValidationError, xy.save)

    def test_nullable(self):
        xy = Country(code="xy")
        xy.nullable = None
        xy.save()

        xy2 = Country.by_code("xy")

        self.assertIsNone(xy2.nullable)

        xy2.nullable = "XY"
        xy2.save()

        xy3 = Country.by_code("xy")

        self.assertEqual(xy3.nullable, "XY")

    def tearDown(self):
        Country.drop_collection()
