"""
Patch for paraspell/xcm-tools Issue #2277:
validateTransact returns the sender/recipient error instead of throwing, so the guard never runs.

This patch modifies the validateTransact function to raise an exception when a sender/recipient error is detected,
ensuring that the guard logic is executed as intended.

Assumptions:
- The original validateTransact function returned an error string or object instead of raising.
- The guard logic is implemented as a decorator or a higher-level function that expects exceptions to be raised.

This patch is pure Python, modular, and contains no external dependencies.
"""

from typing import Any, Dict, Optional


class TransactValidationError(Exception):
    """Custom exception for transact validation errors."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def validateTransact(
    sender: Optional[str],
    recipient: Optional[str],
    amount: Any,
    metadata: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Validates a transact operation, raising on sender/recipient errors.

    Args:
        sender (Optional[str]): The sender's identifier.
        recipient (Optional[str]): The recipient's identifier.
        amount (Any): The amount to transact.
        metadata (Optional[Dict[str, Any]]): Optional metadata.

    Returns:
        bool: True if validation passes.

    Raises:
        TransactValidationError: If sender or recipient is invalid.
    """
    if not sender or not isinstance(sender, str):
        raise TransactValidationError("Invalid sender")
    if not recipient or not isinstance(recipient, str):
        raise TransactValidationError("Invalid recipient")
    # Additional validation logic can be added here
    # For example, check amount is positive, etc.
    if amount is None or (isinstance(amount, (int, float)) and amount <= 0):
        raise TransactValidationError("Invalid amount")
    return True


def guard(func):
    """
    Example guard decorator that catches validation errors.

    Args:
        func (callable): The function to wrap.

    Returns:
        callable: The wrapped function.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TransactValidationError as e:
            # Handle the error as needed, e.g., log or re-raise
            # For demonstration, just return the error message
            return f"Guard caught error: {e.message}"
    return wrapper


@guard
def processTransact(
    sender: Optional[str],
    recipient: Optional[str],
    amount: Any,
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """
    Processes a transact operation after validation.

    Args:
        sender (Optional[str]): The sender's identifier.
        recipient (Optional[str]): The recipient's identifier.
        amount (Any): The amount to transact.
        metadata (Optional[Dict[str, Any]]): Optional metadata.

    Returns:
        str: Success message.
    """
    validateTransact(sender, recipient, amount, metadata)
    # Proceed with transact logic...
    return "Transact processed successfully"


# --- Tests ---

def test_validateTransact():
    # Valid case
    assert validateTransact("alice", "bob", 100) is True

    # Invalid sender
    try:
        validateTransact("", "bob", 100)
        assert False, "Expected TransactValidationError"
    except TransactValidationError as e:
        assert str(e) == "Invalid sender"

    # Invalid recipient
    try:
        validateTransact("alice", None, 100)
        assert False, "Expected TransactValidationError"
    except TransactValidationError as e:
        assert str(e) == "Invalid recipient"

    # Invalid amount
    try:
        validateTransact("alice", "bob", 0)
        assert False, "Expected TransactValidationError"
    except TransactValidationError as e:
        assert str(e) == "Invalid amount"


def test_guard_and_processTransact():
    # Valid case
    result = processTransact("alice", "bob", 100)
    assert result == "Transact processed successfully"

    # Invalid sender
    result = processTransact("", "bob", 100)
    assert result == "Guard caught error: Invalid sender"

    # Invalid recipient
    result = processTransact("alice", None, 100)
    assert result == "Guard caught error: Invalid recipient"

    # Invalid amount
    result = processTransact("alice", "bob", 0)
    assert result == "Guard caught error: Invalid amount"


if __name__ == "__main__":
    test_validateTransact()
    test_guard_and_processTransact()