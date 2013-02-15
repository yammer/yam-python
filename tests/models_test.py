from unittest import TestCase

from yampy.models import GenericModel


class GenericModelTest(TestCase):
    def test_construction_from_json(self):
        model = GenericModel.from_json('{"foo": 1, "bar": {"sub": 2}}')

        self.assertEquals(1, model.foo)
        self.assertEquals(2, model.bar.sub)

    def test_initialization_with_a_dict(self):
        model = GenericModel({"foo": 1})

        self.assertEquals(1, model.foo)

    def test_missing_attributes(self):
        model = GenericModel({"foo": 1})

        with self.assertRaises(AttributeError):
            model.bar
