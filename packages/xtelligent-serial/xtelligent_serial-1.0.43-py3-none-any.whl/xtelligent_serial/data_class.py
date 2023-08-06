from dataclasses import is_dataclass, fields

from .data_structs import register_struct_family, describe_struct_family

descriptor = describe_struct_family('dataclass', is_dataclass, fields)
register_struct_family(descriptor)
