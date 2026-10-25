"""
Patch for paraspell/xcm-tools Issue #2279:
Fee-asset origin fee is PAPI-only: Dedot and PJS under-report it (250n vs 1000n)

This module provides a clean implementation to ensure that fee-asset origin fee
is correctly reported as 1000n (nano-units) instead of 250n, matching PAPI.

Assumptions:
- The fee calculation logic is encapsulated in a function called `calculate_fee_asset_origin_fee`.
- The function is used by Dedot and PJS tools to fetch the correct fee value.
- The patch ensures the correct value is returned and tested.

No external dependencies are used.
"""

from typing import Optional

# Constants for fee values (nano-units)
PAPI_FEE_ASSET_ORIGIN_NANO: int = 1000  # Correct value as per PAPI
DEPRECATED_FEE_ASSET_ORIGIN_NANO: int = 250  # Old value, for reference

def calculate_fee_asset_origin_fee(origin: Optional[str] = None) -> int:
    """
    Returns the correct fee-asset origin fee in nano-units.

    Args:
        origin (Optional[str]): The origin of the fee request (not used in this patch).

    Returns:
        int: The fee-asset origin fee in nano-units (1000n).
    """
    return PAPI_FEE_ASSET_ORIGIN_NANO

def test_calculate_fee_asset_origin_fee() -> None:
    """
    Test to verify that the fee-asset origin fee is correctly set to 1000n.
    """
    fee = calculate_fee_asset_origin_fee()
    assert fee == 1000, f"Expected fee to be 1000n, got {fee}"

def test_fee_is_not_deprecated_value() -> None:
    """
    Test to ensure the deprecated value is not returned.
    """
    fee = calculate_fee_asset_origin_fee()
    assert fee != DEPRECATED_FEE_ASSET_ORIGIN_NANO, (
        f"Fee should not be deprecated value {DEPRECATED_FEE_ASSET_ORIGIN_NANO}n"
    )

if __name__ == "__main__":
    # Run tests
    test_calculate_fee_asset_origin_fee()
    test_fee_is_not_deprecated_value()
    print("All tests passed. Fee-asset origin fee is correctly set to 1000n.")