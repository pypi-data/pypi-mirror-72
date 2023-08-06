from collections import namedtuple
from dataclasses import Field
from typing import Type, Iterable, Any

DescriptorInterface2 = namedtuple('DescriptorInterface', ['name', 'is_instance', 'get_fields'])

class DescriptorInterface:
    '''Describes a family of classes/structs such as dataclass or attrs.'''
    @property
    def name(self) -> str:
        '''Name of the family/API (dataclass, attrs)'''
        raise NotImplementedError()

    def is_instance(self, target: Any) -> bool:
        '''Returns True if an instance is from that family. Note that the API
        may not leverage inheritance for membership.'''
        raise NotImplementedError()

    def get_fields(self, t: Type) -> Iterable[Field]:
        '''Returns the fields of a type in the family/API. The result is an Iterable
        of dataclasses.Field instances.'''
        raise NotImplementedError()


def is_instance_callback(target: Any) -> bool:
    '''Returns true if the target is an instance of the structure family.'''
    raise NotImplementedError()

def get_fields_callback(wanted_type: Type) -> Iterable[Field]:
    '''Returns the fields for the type. Requires that each field is compatible
    with dataclasses.Field.'''
    raise NotImplementedError()

def describe_struct_family(name, is_instance: is_instance_callback, get_fields: get_fields_callback) -> DescriptorInterface:
    return DescriptorInterface2(name, is_instance, get_fields)
