from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional, Union


class FilterCompilationException(Exception):
    pass


class FilterElement(ABC):
    @abstractmethod
    def to_filter_object(self) -> dict:
        """
        Converts the filter element into a filter object for API consumption.
        :return: The JSON object consumed by the API.
        """
        pass


class FilterConditionRelation(Enum):
    """
    Available relations for conditional filters.
    """

    EQUAL = 'equal'
    UNEQUAL = 'unequal'
    GREATER = 'greater'
    LESS = 'less'
    GREATER_EQUAL = 'greaterEqual'
    LESS_EQUAL = 'lessEqual'


class FilterCondition(FilterElement):
    """
    The result will match to this condition. You can find lists or available and valid fields throughout the API.
    Please refer to specific documentation sections for the respective finding methods. Field names are case
    insensitive.
    """

    def to_filter_object(self) -> dict:
        """
        Converts the filter element into a filter object for API consumption.
        :return: The JSON object consumed by the API.
        :raise FilterCompilationException: If the filter did not contain the necessary fields.
        """
        if self.field is not None and self.value is not None:
            return {
                "field": self.field,
                "value": self.value,
                **({"relation": self.relation.value} if self.relation else {}),
            }
        else:
            raise FilterCompilationException(f'Value for field "{self.field}" was not specified.')

    def __init__(
        self, field: str, value: Union[str, int, float, None] = None, relation: FilterConditionRelation = None
    ):
        """
        In its simplest form, the filter parameter takes a field and a value parameter. The field element is restricted
        to a list of field names which vary from listing to listing.

        :param field: refers to the field you want to filter
        :param value: is the argument for that field. By default, the value is a case-insensitive exact match. An
                      asterisk (*) can be used to match an arbitrary number of characters (including zero characters).
        :param relation: The relation element specifies the comparison performed on field and the specific value. It is
                         an optional element and defaults to ‘equal’ if not set. Please see the table below for further
                         details and explanations.

        :example:

        >>> f = FilterCondition('someField').eq('you') & FilterCondition('otherField').ne('me')
        >>> print(f.to_filter_object())
        {'subFilterConnective': 'and', 'subFilter': [{'field': 'someField', 'value': 'you', 'relation': 'equal'},
        {'field': 'otherField', 'value': 'me', 'relation': 'unequal'}]}
        """
        self.field: str = field
        self.value: Union[str, int, float, None] = value
        self.relation: Optional[FilterConditionRelation] = relation

    def eq(self, other: Union[str, int, float]) -> 'FilterCondition':
        """
        Override == setter for value.
        :param other: The value to be set
        :return:
        """
        self.value = other
        self.relation = FilterConditionRelation.EQUAL
        return self

    def ne(self, other: Union[str, int, float]) -> 'FilterCondition':
        """
        Override != setter for value.
        :param other: The value to be set
        :return:
        """
        self.value = other
        self.relation = FilterConditionRelation.UNEQUAL
        return self

    def lt(self, other: Union[str, int, float]) -> 'FilterCondition':
        """
        Override < setter for value.
        :param other: The value to be set
        :return:
        """
        self.value = other
        self.relation = FilterConditionRelation.LESS
        return self

    def le(self, other: Union[str, int, float]) -> 'FilterCondition':
        """
        Override <= setter for value.
        :param other: The value to be set
        :return:
        """
        self.value = other
        self.relation = FilterConditionRelation.LESS_EQUAL
        return self

    def gt(self, other: Union[str, int, float]) -> 'FilterCondition':
        """
        Override > setter for value.
        :param other: The value to be set
        :return:
        """
        self.value = other
        self.relation = FilterConditionRelation.GREATER
        return self

    def ge(self, other: Union[str, int, float]) -> 'FilterCondition':
        """
        Override >= setter for value.
        :param other: The value to be set
        :return:
        """
        self.value = other
        self.relation = FilterConditionRelation.GREATER_EQUAL
        return self

    def startswith(self, begin: str) -> 'FilterCondition':
        """
        Filter for entries starting with a specific pattern
        :param begin: The begin filter
        :return:
        """
        self.value = f"{begin}*"
        self.relation = FilterConditionRelation.EQUAL
        return self

    def contains(self, value: str) -> 'FilterCondition':
        """
        Filter condition with contains semantic. Filters for entities that contain the given value
        :param value: The contain filter value
        :return:
        """
        self.value = f"*{value}*"
        self.relation = FilterConditionRelation.EQUAL
        return self

    def __and__(self, other: FilterElement) -> 'FilterChain':
        """
        Dynamically construct a 'and' filter chain object using binary operations.
        :param other: The other filter element to chain to this element.
        :return:
        """
        if isinstance(other, FilterCondition):
            return FilterChain(FilterChainConnective.AND).add_filter(self).add_filter(other)
        elif isinstance(other, FilterChain):
            if other.connective == FilterChainConnective.AND:
                return other.add_filter(self)
            elif other.connective == FilterChainConnective.OR:
                return FilterChain(FilterChainConnective.AND).add_filter(self).add_filter(other)
            else:
                raise FilterCompilationException('Unknown filter element connective operation')
        else:
            raise FilterCompilationException('Unknown filter element type')

    def __or__(self, other: FilterElement) -> 'FilterChain':
        """
        Dynamically construct a 'or' filter chain object using binary operations.
        :param other: The other filter element to chain to this element.
        :return: A FilterChain implementation for the given logic.
        """
        if isinstance(other, FilterCondition):
            return FilterChain(FilterChainConnective.OR).add_filter(self).add_filter(other)
        elif isinstance(other, FilterChain):
            if other.connective == FilterChainConnective.OR:
                return other.add_filter(self)
            elif other.connective == FilterChainConnective.AND:
                return FilterChain(FilterChainConnective.OR).add_filter(self).add_filter(other)
            else:
                raise FilterCompilationException('Unknown filter element connective operation')
        else:
            raise FilterCompilationException('Unknown filter element type')


class FilterChainConnective(Enum):
    """
    Available connectives for chain filters.
    """

    AND = 'and'
    OR = 'or'


class FilterChain(FilterElement):
    """
    Construct a filter chain containing multiple filter conditions. Supports a connective relation to be set. Supported
    are AND and OR connectives.
    """

    def to_filter_object(self) -> dict:
        """
        Recursively builds the filter objects to be constructed.
        :return:
        """

        if len(self.filters) == 0:
            raise FilterCompilationException('ChainFilter has no filters attached.')

        return {"subFilterConnective": self.connective.value, "subFilter": [f.to_filter_object() for f in self.filters]}

    def __init__(self, connective: FilterChainConnective):
        """
        Start a new filter chain. You will have to set the connective at the very least.
        :param connective: The connective to use for this chain. Either 'and' or 'or'.
        """
        self.connective: FilterChainConnective = connective
        self.filters: List[FilterElement] = []

    def add_filter(self, filter_element: FilterElement, front: bool = False) -> 'FilterChain':
        """
        Add a new filter element into this chain.
        :param filter_element: The element to add to the filter chain.
        :param front: Insert the element in the front of the array
        :return: This object in order to chain add_filter operations together
        """
        if front:
            self.filters.insert(0, filter_element)
        else:
            self.filters.append(filter_element)

        return self

    def __and__(self, other: FilterElement) -> 'FilterChain':
        """
        Dynamically construct a 'and' filter chain object using binary operations.
        :param other: The other filter element to chain to this element.
        :return:
        """
        if isinstance(other, FilterCondition):
            if self.connective == FilterChainConnective.AND:
                return self.add_filter(other)
            elif self.connective == FilterChainConnective.OR:
                return FilterChain(FilterChainConnective.AND).add_filter(self).add_filter(other)
            else:
                raise FilterCompilationException('Unknown filter element connective operation')
        elif isinstance(other, FilterChain):
            if self.connective == FilterChainConnective.AND and other.connective == FilterChainConnective.AND:
                # filters can be merged
                for f in other.filters:
                    self.add_filter(f)
                return self
            elif self.connective == FilterChainConnective.AND and other.connective == FilterChainConnective.OR:
                return self.add_filter(other)
            elif self.connective == FilterChainConnective.OR and other.connective == FilterChainConnective.AND:
                return other.add_filter(self, True)
            elif self.connective == FilterChainConnective.OR and other.connective == FilterChainConnective.OR:
                return FilterChain(FilterChainConnective.AND).add_filter(self).add_filter(other)
            else:
                raise FilterCompilationException('Unknown filter element connective operation')
        else:
            raise FilterCompilationException('Unknown filter element type')

    def __or__(self, other: FilterElement) -> 'FilterChain':
        """
        Dynamically construct a 'and' filter chain object using binary operations.
        :param other: The other filter element to chain to this element.
        :return:
        """
        if isinstance(other, FilterCondition):
            if self.connective == FilterChainConnective.OR:
                return self.add_filter(other)
            elif self.connective == FilterChainConnective.AND:
                return FilterChain(FilterChainConnective.OR).add_filter(self).add_filter(other)
            else:
                raise FilterCompilationException('Unknown filter element connective operation')
        elif isinstance(other, FilterChain):
            if self.connective == FilterChainConnective.OR and other.connective == FilterChainConnective.OR:
                # filters can be merged
                for f in other.filters:
                    self.add_filter(f)
                return self
            elif self.connective == FilterChainConnective.OR and other.connective == FilterChainConnective.AND:
                return self.add_filter(other)
            elif self.connective == FilterChainConnective.AND and other.connective == FilterChainConnective.OR:
                return other.add_filter(self, True)
            elif self.connective == FilterChainConnective.AND and other.connective == FilterChainConnective.AND:
                return FilterChain(FilterChainConnective.OR).add_filter(self).add_filter(other)
            else:
                raise FilterCompilationException('Unknown filter element connective operation')
        else:
            raise FilterCompilationException('Unknown filter element type')
