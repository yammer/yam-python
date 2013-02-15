from unittest import TestCase

from yampy.models import GenericModel, extract_id


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


class ExtractIDTest(TestCase):
    def test_extraction_from_dict(self):
        object_id = extract_id({"id": 17})
        self.assertEquals(17, object_id)

    def test_extraction_from_attribute(self):
        object_id = extract_id(GenericModel({"id": 21}))
        self.assertEquals(21, object_id)

    def test_fallback_when_extraction_fails(self):
        object_id = extract_id(37)
        self.assertEquals(37, object_id)
