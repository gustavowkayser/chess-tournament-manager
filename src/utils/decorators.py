from typing import Callable, Any

def type_check(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to enforce type checking based on function annotations."""
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        annotations = func.__annotations__
        result = func(*args, **kwargs)
        for arg_name, arg_value in args[0].__dict__.items():
            expected_type = annotations.get(arg_name)
            if expected_type is not None and not isinstance(arg_value, expected_type):
                print(f"Argument '{arg_name}' is not of type {expected_type}")
        return result
    return wrapper