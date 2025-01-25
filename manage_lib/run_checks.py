from typing import Callable, List, Tuple, Optional

def run_checks(checks: List[Callable[[], Tuple[bool, Optional[str]]]]) -> bool:
    """
    Runs a list of checks and prints the result of each.
    
    Args:
        checks (List[Callable[[], Tuple[bool, Optional[str]]]]): List of check functions.

    Returns:
        bool: True if all checks pass, False otherwise.
    """
    all_passed = True

    for check in checks:
        # Get the function name for display
        check_name = check.__name__

        # Run the check
        result, error_message = check()

        if result:
            print(f"✅ {check_name} passed.")
        else:
            print(f"❌ {check_name} failed: {error_message}")
            all_passed = False

    return all_passed

