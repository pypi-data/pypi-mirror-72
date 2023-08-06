from dataclasses import fields

import attr
from .fixtures import DataClass, AttrsClass, dataclass_descriptor, attrs_descriptor  # pylint: disable=unused-import

# pylint: disable=redefined-outer-name

def test_dataclass_descript(dataclass_descriptor):
    d = dataclass_descriptor
    assert d.is_instance(DataClass(1, 'x'))
    assert d.get_fields(DataClass)
    assert d.get_fields(DataClass) == fields(DataClass)


def test_attrs_descript(attrs_descriptor):
    d = attrs_descriptor
    assert d.is_instance(AttrsClass(1, 'x'))
    assert d.get_fields(AttrsClass)
    assert d.get_fields(AttrsClass) == attr.fields(AttrsClass)
