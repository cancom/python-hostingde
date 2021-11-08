import marshmallow_dataclass
from marshmallow import post_dump, Schema


def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class CamelCaseSchema(Schema):
    """Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """

    SKIP_VALUES = {None}

    def __init__(self, **kwargs):
        super().__init__(unknown='EXCLUDE', **kwargs)

    def on_bind_field(self, field_name, field_obj):
        """Use lower-camel-casing as external representation"""
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

    @post_dump
    def remove_skip_values(self, data, **kwargs):
        """
        Remove None values from the serialization result
        :param data: The input data (dict). Already serialized, but may contain None values
        :param kwargs: Required by overwrite
        :return: Transformed data with None values removed
        """
        return {
            key: value
            for key, value in data.items()
            if isinstance(value, list) or isinstance(value, dict) or value not in self.SKIP_VALUES
        }


class Model:
    """Represents a basic API Resource model"""

    @classmethod
    def get_class_instance(cls):
        return cls

    def to_json(self):
        return marshmallow_dataclass.class_schema(self.get_class_instance(), base_schema=CamelCaseSchema)().dump(self)

    def __init__(self, **kwargs):
        """
        Default constructor that sets all kwargs as internal properties
        :param kwargs: dictionary of parameters that this class must support
        """
        self.__dict__ = kwargs

    @classmethod
    def from_json(cls, data: dict) -> 'Model':
        """
        Create a new object from a given JSON.
        :param data: The json data
        :return: New instance of the class
        """
        return marshmallow_dataclass.class_schema(cls, base_schema=CamelCaseSchema)().load(data)
