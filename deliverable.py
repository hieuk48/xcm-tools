from typing import Any, Dict, Union, List

def is_numeric_string(value: Any) -> bool:
    """
    Check if the value is a string that represents a numeric value.
    """
    return isinstance(value, str) and value.isdigit()

def transform_currency_id(obj: Any) -> Any:
    """
    Recursively traverse the input object and ensure that string numeric 'currency_id'
    fields in multi-key objects are preserved as strings and not mangled or converted.

    Args:
        obj: The input object (dict, list, or primitive).

    Returns:
        The transformed object with correct 'currency_id' handling.
    """
    if isinstance(obj, dict):
        new_obj = {}
        for k, v in obj.items():
            # If the key is 'currency_id' and value is a numeric string, preserve as string
            if k == 'currency_id' and is_numeric_string(v):
                new_obj[k] = v
            else:
                new_obj[k] = transform_currency_id(v)
        return new_obj
    elif isinstance(obj, list):
        return [transform_currency_id(item) for item in obj]
    else:
        return obj

def transform(data: Any) -> Any:
    """
    Public API for transforming the input data structure, ensuring that
    string numeric 'currency_id' fields are not mangled.

    Args:
        data: The input data structure.

    Returns:
        The transformed data structure.
    """
    return transform_currency_id(data)

# --- TESTS ---

def _test():
    """
    Run basic tests to verify transform() behavior.
    """
    # Test 1: currency_id as string numeric in multi-key dict
    input1 = {
        "currency_id": "123",
        "amount": 1000,
        "meta": {
            "currency_id": "456",
            "other": 1
        }
    }
    output1 = transform(input1)
    assert output1["currency_id"] == "123"
    assert output1["meta"]["currency_id"] == "456"

    # Test 2: currency_id as int (should remain int)
    input2 = {
        "currency_id": 789,
        "amount": 1000
    }
    output2 = transform(input2)
    assert output2["currency_id"] == 789

    # Test 3: Nested list of dicts
    input3 = [
        {"currency_id": "101112", "amount": 5},
        {"currency_id": 131415, "amount": 6}
    ]
    output3 = transform(input3)
    assert output3[0]["currency_id"] == "101112"
    assert output3[1]["currency_id"] == 131415

    # Test 4: currency_id not present
    input4 = {"foo": "bar"}
    output4 = transform(input4)
    assert output4 == {"foo": "bar"}

    # Test 5: currency_id as non-numeric string
    input5 = {"currency_id": "USD"}
    output5 = transform(input5)
    assert output5["currency_id"] == "USD"

    print("All tests passed.")

if __name__ == "__main__":
    _test()