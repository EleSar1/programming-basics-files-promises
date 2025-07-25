from functools import wraps


def only_str_in_list(func):

    """
    Decorator that ensures the 'data' argument passed to the decorated function
    is a list containing only strings.

    Raises:
        TypeError: If 'data' is not a list or if it contains any non-string elements.
    """
        
    @wraps(func)
    def wrapper(data):

        if not isinstance(data, list):
            raise TypeError("Expected a list for data.")

        for item in data:
            if not isinstance(item, str):
                raise TypeError("Found a non-string inside data.")
        
        return func(data)
    
    return wrapper
