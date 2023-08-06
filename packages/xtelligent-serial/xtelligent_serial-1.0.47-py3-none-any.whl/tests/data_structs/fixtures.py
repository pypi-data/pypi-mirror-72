from dataclasses import is_dataclass, fields, dataclass

import attr
import pytest

from xtelligent_serial.data_structs.struct_descriptor import describe_struct_family

@dataclass
class DataClass:
    a: int
    b: str

@pytest.fixture
def dataclass_descriptor():
    return describe_struct_family('dataclass', is_dataclass, fields)

@attr.s
class AttrsClass:
    a = attr.ib(validator=attr.validators.instance_of(int))
    b = attr.ib(validator=attr.validators.instance_of(str))

@pytest.fixture
def attrs_descriptor():
    return describe_struct_family('attrs', attr.has, attr.fields)
