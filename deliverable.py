"""
Patch for paraspell/xcm-tools: Fix getDryRunCall to respect Astar XcmPaymentApi condition.

This patch ensures that for Astar (and Shiden/Shibuya) chains, the dry run call uses the
XcmPaymentApi to estimate fees, instead of falling back to paymentInfo. This is necessary
because Astar's runtime requires a special API for accurate fee estimation.

This code is a Python adaptation for demonstration and testing purposes.
"""

from typing import Any, Dict, Optional

# Simulated chain constants for Astar, Shiden, Shibuya
ASTAR_CHAIN_IDS = {
    "astar": 2006,
    "shiden": 2007,
    "shibuya": 2008,
}

def is_astar_chain(chain_id: int) -> bool:
    """
    Returns True if the chain_id is one of the Astar family chains.
    """
    return chain_id in ASTAR_CHAIN_IDS.values()

def get_xcm_payment_api_fee(call: Dict[str, Any], api: Any) -> int:
    """
    Simulate querying the XcmPaymentApi for fee estimation.
    """
    # In actual implementation, this would call the chain's runtime API.
    # Here, we simulate a fixed fee for demonstration.
    return 123456  # Dummy fee value

def get_payment_info_fee(call: Dict[str, Any], api: Any) -> int:
    """
    Simulate querying paymentInfo for fee estimation.
    """
    # In actual implementation, this would call paymentInfo.
    return 654321  # Dummy fee value

def get_dry_run_call(
    call: Dict[str, Any],
    api: Any,
    chain_id: int,
    use_xcm_payment_api: Optional[bool] = None
) -> int:
    """
    Returns the estimated fee for a call, using the correct API for the chain.

    For Astar family chains, always use XcmPaymentApi.
    For others, use paymentInfo unless use_xcm_payment_api is True.
    """
    if is_astar_chain(chain_id):
        # Always use XcmPaymentApi for Astar, Shiden, Shibuya
        return get_xcm_payment_api_fee(call, api)
    elif use_xcm_payment_api:
        return get_xcm_payment_api_fee(call, api)
    else:
        return get_payment_info_fee(call, api)

# --- Tests ---

def test_get_dry_run_call():
    class DummyApi:
        pass

    dummy_call = {"section": "xcmPallet", "method": "send", "args": {}}
    api = DummyApi()

    # Test for Astar
    astar_fee = get_dry_run_call(dummy_call, api, ASTAR_CHAIN_IDS["astar"])
    assert astar_fee == 123456, "Astar should use XcmPaymentApi"

    # Test for Shiden
    shiden_fee = get_dry_run_call(dummy_call, api, ASTAR_CHAIN_IDS["shiden"])
    assert shiden_fee == 123456, "Shiden should use XcmPaymentApi"

    # Test for Shibuya
    shibuya_fee = get_dry_run_call(dummy_call, api, ASTAR_CHAIN_IDS["shibuya"])
    assert shibuya_fee == 123456, "Shibuya should use XcmPaymentApi"

    # Test for other chain, default (should use paymentInfo)
    other_chain_fee = get_dry_run_call(dummy_call, api, 1000)
    assert other_chain_fee == 654321, "Other chains should use paymentInfo by default"

    # Test for other chain, but force XcmPaymentApi
    other_chain_xcm_fee = get_dry_run_call(dummy_call, api, 1000, use_xcm_payment_api=True)
    assert other_chain_xcm_fee == 123456, "Other chains should use XcmPaymentApi if forced"

    print("All tests passed.")

if __name__ == "__main__":
    test_get_dry_run_call()