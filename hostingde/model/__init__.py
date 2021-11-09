from typing import Any, Optional, Type, TypeVar

import marshmallow_dataclass
from marshmallow import post_dump, post_load, Schema
from marshmallow.fields import Field

import hostingde


def camelcase(s: str) -> str:
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class CamelCaseSchema(Schema):
    """Schema that uses camel-case for its external representation
    and snake-case for its internal representation.
    """

    SKIP_VALUES = {None}

    def __init__(self, **kwargs: Any):
        super().__init__(unknown='EXCLUDE', **kwargs)

    def on_bind_field(self, field_name: str, field_obj: Field) -> None:
        """Use lower-camel-casing as external representation"""
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

    @post_load
    def post_load(self, data: Any, **kwargs: Any) -> Any:
        data["context"] = self.context.get('client', None)
        return data

    @post_dump
    def remove_skip_values(self, data: dict, **kwargs: dict) -> dict:
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


T = TypeVar('T', bound='Model')


class Model:
    """Represents a basic API Resource model"""

    @classmethod
    def get_class_instance(cls: Type[T]) -> Type[T]:
        return cls

    def to_json(self) -> dict:
        return marshmallow_dataclass.class_schema(self.get_class_instance(), base_schema=CamelCaseSchema)().dump(self)

    def __init__(self, **kwargs: Any):
        """
        Default constructor that sets all kwargs as internal properties

        All models allow for the context to be set.

        :param kwargs: dictionary of parameters that this class must support
        """
        self.__dict__ = kwargs
        self.client: Optional[hostingde.HostingDeClient] = None

        # Context might be provided as a kwarg
        if "context" in kwargs and isinstance(kwargs["context"], hostingde.HostingDeClient):
            self.client = kwargs["context"]

    @classmethod
    def from_json(cls: Type[T], data: dict, client: 'hostingde.HostingDeClient' = None) -> T:
        """
        Create a new object from a given JSON.
        :param data: The json data
        :param client: The client to use for this object
        :return: New instance of the class
        """
        return marshmallow_dataclass.class_schema(cls, base_schema=CamelCaseSchema)(context={'client': client}).load(
            data
        )
