def split_fields(lines: list):

    return [line.split(",") for line in lines]
        


def sort_lines(lines: list, field_key: int, reverse: bool = False, numeric: bool=False) -> list:

    """
    Sorts a list of lists based on the element at the specified field index.

    Args:
        lines (list): List of lists to sort.
        field_key (int): Index of the field to sort by.
        reverse (bool, optional): Sort in descending order if True. Defaults to False.
        numeric (bool, optional): If True, sort fields as floating-point numbers. Defaults to False.

    Returns:
        list: Sorted list of lists.
    """

    lines = split_fields(lines)

    if numeric:
        sorted_lines = sorted(lines, key=lambda line: float(line[field_key]), reverse=reverse)
    else:
        sorted_lines = sorted(lines, key=lambda line: line[field_key], reverse=reverse)

    return [",".join(line) for line in sorted_lines]