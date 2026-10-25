"""
Patch for paraspell/xcm-tools: AssetHub swap respects user slippage and protects destination amount.

This module provides a function to compute the minimum acceptable destination amount
based on user-specified slippage, and validates swap execution accordingly.

This is a pure Python implementation for demonstration and testing purposes.
"""

from typing import Optional


def calculate_min_destination_amount(
    expected_amount: float,
    slippage_percent: float
) -> float:
    """
    Calculate the minimum acceptable destination amount based on user slippage.

    Args:
        expected_amount (float): The expected amount to receive from the swap.
        slippage_percent (float): The maximum slippage allowed by the user (as a percentage, e.g., 1.0 for 1%).

    Returns:
        float: The minimum acceptable destination amount.

    Raises:
        ValueError: If slippage_percent is negative or expected_amount is negative.
    """
    if expected_amount < 0:
        raise ValueError("Expected amount cannot be negative.")
    if slippage_percent < 0:
        raise ValueError("Slippage percent cannot be negative.")

    min_amount = expected_amount * (1 - slippage_percent / 100)
    return min_amount


def execute_swap(
    offered_amount: float,
    expected_destination_amount: float,
    user_slippage_percent: float,
    actual_destination_amount: float
) -> bool:
    """
    Execute a swap, ensuring the actual destination amount respects user slippage.

    Args:
        offered_amount (float): The amount offered for the swap.
        expected_destination_amount (float): The expected amount to receive.
        user_slippage_percent (float): The user's allowed slippage percent.
        actual_destination_amount (float): The actual amount to be received.

    Returns:
        bool: True if the swap is valid and executed, False otherwise.

    Raises:
        ValueError: If any input is negative.
    """
    if offered_amount < 0 or expected_destination_amount < 0 or user_slippage_percent < 0 or actual_destination_amount < 0:
        raise ValueError("Amounts and slippage percent must be non-negative.")

    min_acceptable = calculate_min_destination_amount(expected_destination_amount, user_slippage_percent)
    if actual_destination_amount >= min_acceptable:
        # Swap is valid and executed
        return True
    else:
        # Swap is rejected due to slippage protection
        return False


# --- TESTS ---

def _test_calculate_min_destination_amount() -> None:
    assert abs(calculate_min_destination_amount(1000, 1.0) - 990.0) < 1e-6
    assert abs(calculate_min_destination_amount(500, 0.5) - 497.5) < 1e-6
    assert abs(calculate_min_destination_amount(200, 0.0) - 200.0) < 1e-6

    try:
        calculate_min_destination_amount(-100, 1.0)
        assert False, "Negative expected_amount should raise"
    except ValueError:
        pass

    try:
        calculate_min_destination_amount(100, -1.0)
        assert False, "Negative slippage_percent should raise"
    except ValueError:
        pass


def _test_execute_swap() -> None:
    # Valid swap
    assert execute_swap(1000, 1000, 1.0, 995.0) is True
    # At minimum
    assert execute_swap(1000, 1000, 1.0, 990.0) is True
    # Below minimum
    assert execute_swap(1000, 1000, 1.0, 989.9) is False

    # Zero slippage
    assert execute_swap(1000, 1000, 0.0, 1000.0) is True
    assert execute_swap(1000, 1000, 0.0, 999.9) is False

    # Negative values
    try:
        execute_swap(-1000, 1000, 1.0, 995.0)
        assert False, "Negative offered_amount should raise"
    except ValueError:
        pass

    try:
        execute_swap(1000, -1000, 1.0, 995.0)
        assert False, "Negative expected_destination_amount should raise"
    except ValueError:
        pass

    try:
        execute_swap(1000, 1000, -1.0, 995.0)
        assert False, "Negative user_slippage_percent should raise"
    except ValueError:
        pass

    try:
        execute_swap(1000, 1000, 1.0, -995.0)
        assert False, "Negative actual_destination_amount should raise"
    except ValueError:
        pass


if __name__ == "__main__":
    _test_calculate_min_destination_amount()
    _test_execute_swap()
    print("All tests passed.")