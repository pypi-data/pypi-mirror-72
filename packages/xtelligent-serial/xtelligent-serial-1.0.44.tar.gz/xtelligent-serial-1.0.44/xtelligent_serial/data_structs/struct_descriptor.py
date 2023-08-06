from collections import namedtuple
from dataclasses import Field
from typing import Type, Iterable, Any

DescriptorInterface = namedtuple('DescriptorInterface', ['name', 'is_instance', 'get_fields'])
''' Describes a family of classes/structs such as dataclass or attrs.

    name: Name of the family/API (dataclass, attrs)
    is_instance: Returns True if an instance is from that family. Note that the API
        may not depend on inheritance for membership.
    get_fields: Returns the fields of a type in the family/API. The result is an Iterable
        of dataclasses.Field instances.
'''

def is_instance_callback(target: Any) -> bool:
    '''Returns true if the target is an instance of the structure family.'''
    raise NotImplementedError()

def get_fields_callback(wanted_type: Type) -> Iterable[Field]:
    '''Returns the fields for the type. Requires that each field is compatible
    with dataclasses.Field.'''
    raise NotImplementedError()

def describe_struct_family(name, is_instance: is_instance_callback, get_fields: get_fields_callback) -> DescriptorInterface:
    return DescriptorInterface(name, is_instance, get_fields)
