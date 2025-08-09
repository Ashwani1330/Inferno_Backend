def parse_age(age_str: str) -> int:
    """Parses an age string (e.g., '18-25' or '30') to a numeric value."""

    if "-" in age_str:
        try:
            low, high = map(int, age_str.split("-"))
            return (low + high) // 2
        except ValueError:
            return 25  # Default age of parsing

    # If not a range; rather direct age    
    try:
        return int(age_str)
    except ValueError:
        return 25  # Default age if parsing fails
