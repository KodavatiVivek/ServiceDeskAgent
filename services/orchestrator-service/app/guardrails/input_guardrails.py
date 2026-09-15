FORBIDDEN_PATTERNS = [
    "ignore previous instructions",
    "show me passwords",
    "dump secrets",
    "bypass approval",
]

def validate_input(user_query: str) -> tuple[bool, str | None]:
    q = user_query.lower()
    for pattern in FORBIDDEN_PATTERNS:
        if pattern in q:
            return False, f"Blocked unsafe request pattern: {pattern}"
    return True, None
