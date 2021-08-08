"""Always Array Validator"""
# standard library
from typing import Iterator, Union

# first-party
from tcex.input.field_types.entity_array_type import EntityArrayType
from tcex.input.field_types.utils import ti_utils


class IndicatorArray(EntityArrayType):
    """IndicatorArray Field Types"""

    # TODO: [med] check with Matt on where these need to be defined (parent/child)?
    __input_type__ = 'String'
    __playbook_data_type__ = ['String', 'StringArray', 'TCEntity', 'TCEntityArray']
    _optional = False

    @classmethod
    def _auto_filter(cls, items: list) -> Iterator[Union[dict, str]]:
        """Auto filter list - only include specific types."""
        for item in items:
            if isinstance(item, dict):  # TCEntity
                if 'type' in item and item.get('type') in ti_utils().indicator_types:
                    yield item
            else:
                # not a TCEntity so no filter required
                yield item


class IndicatorArrayOptional(IndicatorArray):
    """Optional IndicatorArray Field Types.

    When using IndicatorArrayOptional type it must also
    be options -> Optional[IndicatorArrayOptional].
    """

    _optional = True
