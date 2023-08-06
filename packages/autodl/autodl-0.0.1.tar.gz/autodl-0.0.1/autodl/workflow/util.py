
def same_code(obj1: object, obj2: object, method_name: str) -> bool:
    """Verify that 2 objects have the same code for the same method name.

    Args:
        obj1 (object): first object.
        obj2 (object): second object.
        method_name (str): name of the method to check.

    Returns:
        bool: True if both methods have the same code. False otherwise.
    """
    method_obj1 = getattr(obj1, method_name)
    method_obj2 = getattr(obj2, method_name)

    return method_obj1.__code__ == method_obj2.__code__
