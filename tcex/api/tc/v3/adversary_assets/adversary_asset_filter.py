"""Adversary_Asset TQL Filter"""
# standard library
from enum import Enum

# first-party
from tcex.api.tc.v3.api_endpoints import ApiEndpoints
from tcex.api.tc.v3.filter_abc import FilterABC
from tcex.api.tc.v3.tql.tql import Tql
from tcex.api.tc.v3.tql.tql_operator import TqlOperator
from tcex.api.tc.v3.tql.tql_type import TqlType


class AdversaryAssetFilter(FilterABC):
    """Filter Object for AdversaryAssets"""

    @property
    def _api_endpoint(self) -> str:
        """Return the API endpoint."""
        return ApiEndpoints.ADVERSARY_ASSETS.value

    def asset(self, operator: Enum, asset: str) -> None:
        """Filter Asset based on **asset** keyword.

        Args:
            operator: The operator enum for the filter.
            asset: The sub-type of the victim asset.
        """
        self._tql.add_filter('asset', operator, asset, TqlType.STRING)

    def associated_group(self, operator: Enum, associated_group: int) -> None:
        """Filter associatedGroup based on **associatedGroup** keyword.

        Args:
            operator: The operator enum for the filter.
            associated_group: None.
        """
        self._tql.add_filter('associatedGroup', operator, associated_group, TqlType.INTEGER)

    @property
    def has_group(self):
        """Return **GroupFilter** for further filtering."""
        # first-party
        from tcex.api.tc.v3.groups.group_filter import GroupFilter

        groups = GroupFilter(Tql())
        self._tql.add_filter('hasGroup', TqlOperator.EQ, groups, TqlType.SUB_QUERY)
        return groups

    @property
    def has_indicator(self):
        """Return **IndicatorFilter** for further filtering."""
        # first-party
        from tcex.api.tc.v3.indicators.indicator_filter import IndicatorFilter

        indicators = IndicatorFilter(Tql())
        self._tql.add_filter('hasIndicator', TqlOperator.EQ, indicators, TqlType.SUB_QUERY)
        return indicators

    def has_victim(self, operator: Enum, has_victim: int) -> None:
        """Filter Associated Victim based on **hasVictim** keyword.

        Args:
            operator: The operator enum for the filter.
            has_victim: A nested query for association to other victims.
        """
        self._tql.add_filter('hasVictim', operator, has_victim, TqlType.INTEGER)

    def has_victim_asset(self, operator: Enum, has_victim_asset: int) -> None:
        """Filter Associated Victim Asset based on **hasVictimAsset** keyword.

        Args:
            operator: The operator enum for the filter.
            has_victim_asset: A nested query for association to other victim assets.
        """
        self._tql.add_filter('hasVictimAsset', operator, has_victim_asset, TqlType.INTEGER)

    def id(self, operator: Enum, id: int) -> None:  # pylint: disable=redefined-builtin
        """Filter ID based on **id** keyword.

        Args:
            operator: The operator enum for the filter.
            id: The ID of the victim asset.
        """
        self._tql.add_filter('id', operator, id, TqlType.INTEGER)

    def owner(self, operator: Enum, owner: int) -> None:
        """Filter Owner ID based on **owner** keyword.

        Args:
            operator: The operator enum for the filter.
            owner: The owner ID of the victim.
        """
        self._tql.add_filter('owner', operator, owner, TqlType.INTEGER)

    def owner_name(self, operator: Enum, owner_name: str) -> None:
        """Filter Owner Name based on **ownerName** keyword.

        Args:
            operator: The operator enum for the filter.
            owner_name: The owner name of the victim.
        """
        self._tql.add_filter('ownerName', operator, owner_name, TqlType.STRING)

    def summary(self, operator: Enum, summary: str) -> None:
        """Filter Summary based on **summary** keyword.

        Args:
            operator: The operator enum for the filter.
            summary: The name of the victim asset.
        """
        self._tql.add_filter('summary', operator, summary, TqlType.STRING)

    def type(self, operator: Enum, type: int) -> None:  # pylint: disable=redefined-builtin
        """Filter Type ID based on **type** keyword.

        Args:
            operator: The operator enum for the filter.
            type: The ID of the victim asset type.
        """
        self._tql.add_filter('type', operator, type, TqlType.INTEGER)

    def type_name(self, operator: Enum, type_name: str) -> None:
        """Filter Type Name based on **typeName** keyword.

        Args:
            operator: The operator enum for the filter.
            type_name: The name of the victim asset type.
        """
        self._tql.add_filter('typeName', operator, type_name, TqlType.STRING)

    def victim_id(self, operator: Enum, victim_id: int) -> None:
        """Filter Victim ID based on **victimId** keyword.

        Args:
            operator: The operator enum for the filter.
            victim_id: The ID of the victim the victim asset is applied to.
        """
        self._tql.add_filter('victimId', operator, victim_id, TqlType.INTEGER)

    def victim_name(self, operator: Enum, victim_name: str) -> None:
        """Filter Victim Name based on **victimName** keyword.

        Args:
            operator: The operator enum for the filter.
            victim_name: The name of the victim.
        """
        self._tql.add_filter('victimName', operator, victim_name, TqlType.STRING)