from typing import Any, Dict, List, Optional, Tuple


class DuplicateAssetLocationError(Exception):
    """Exception raised when duplicate asset locations are found during lookup."""
    def __init__(self, asset_location: Any, matches: List[Any]) -> None:
        super().__init__(
            f"Duplicate asset location found for {asset_location}: {matches}"
        )
        self.asset_location = asset_location
        self.matches = matches


class AssetRegistry:
    """
    Registry for asset locations with duplicate guard.

    This class allows registering asset locations and looking them up.
    If duplicate asset locations are found during lookup, an exception is raised.
    """

    def __init__(self) -> None:
        # Mapping from asset location identifier to list of asset data
        self._assets: Dict[Any, List[Any]] = {}

    def register_asset(self, location: Any, asset_data: Any) -> None:
        """
        Register an asset at a given location.

        Args:
            location: The identifier for the asset location.
            asset_data: The data associated with the asset.
        """
        if location not in self._assets:
            self._assets[location] = []
        self._assets[location].append(asset_data)

    def lookup_asset(self, location: Any) -> Optional[Any]:
        """
        Lookup an asset by location.

        Args:
            location: The identifier for the asset location.

        Returns:
            The asset data if found and unique, None if not found.

        Raises:
            DuplicateAssetLocationError: If multiple assets are found for the location.
        """
        matches = self._assets.get(location, [])
        if not matches:
            return None
        if len(matches) > 1:
            raise DuplicateAssetLocationError(location, matches)
        return matches[0]

    def all_assets(self) -> List[Tuple[Any, Any]]:
        """
        Returns all registered assets as a list of (location, asset_data) tuples.
        """
        result: List[Tuple[Any, Any]] = []
        for location, assets in self._assets.items():
            for asset in assets:
                result.append((location, asset))
        return result


# --- TESTS ---

def test_asset_registry_unique_lookup() -> None:
    registry = AssetRegistry()
    registry.register_asset("location1", {"symbol": "ABC"})
    assert registry.lookup_asset("location1") == {"symbol": "ABC"}
    assert registry.lookup_asset("location2") is None

def test_asset_registry_duplicate_guard() -> None:
    registry = AssetRegistry()
    registry.register_asset("location1", {"symbol": "ABC"})
    registry.register_asset("location1", {"symbol": "DEF"})
    try:
        registry.lookup_asset("location1")
        assert False, "Expected DuplicateAssetLocationError"
    except DuplicateAssetLocationError as e:
        assert e.asset_location == "location1"
        assert len(e.matches) == 2

def test_asset_registry_all_assets() -> None:
    registry = AssetRegistry()
    registry.register_asset("locA", 1)
    registry.register_asset("locB", 2)
    registry.register_asset("locA", 3)
    assets = registry.all_assets()
    assert ("locA", 1) in assets
    assert ("locA", 3) in assets
    assert ("locB", 2) in assets
    assert len(assets) == 3

if __name__ == "__main__":
    test_asset_registry_unique_lookup()
    test_asset_registry_duplicate_guard()
    test_asset_registry_all_assets()
    print("All tests passed.")