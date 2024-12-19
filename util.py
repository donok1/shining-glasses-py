def assert_type(value, expected_type):
    if not isinstance(value, expected_type):
        raise ValueError(f"Expected {expected_type}, got {type(value)}")

def assert_int_range(value, min_value, max_value):
    if not min_value <= value <= max_value:
        raise ValueError(f"Expected {min_value} <= value <= {max_value}, got {value}")

def assert_equal(value, expected_value):
    if value != expected_value:
        raise ValueError(f"Expected {expected_value}, got {value}")