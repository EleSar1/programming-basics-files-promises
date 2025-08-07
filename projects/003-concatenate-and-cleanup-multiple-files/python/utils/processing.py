from utils.decorators import only_str_in_list
from utils.io_utils import load_lines


@only_str_in_list
def concatenate_data(file_paths: list) -> list:

    """
    Reads and concatenates the contents of multiple text files into a single list of lines.

    Args:
        file_paths (list): A list of file paths (strings) to be read.

    Returns:
        lines (list): A list containing all lines from the given files, in order.

    Raises:
        TypeError: If 'file_paths' is not a list of strings (enforced by the decorator).
        FileNotFoundError, PermissionError: If a file cannot be accessed.
    """
    
    lines = []

    for file_path in file_paths:

        data = load_lines(file_path)
        lines.extend(data)
    
    return lines


@only_str_in_list
def save_header(lines: list) -> list:

    """
    Extracts and returns the first line of a list as the header, 
    removing only leading and trailing spaces (but not newlines).

    Args:
        lines (list): A list of strings representing lines from a file.

    Returns:
        list: A list containing the first line with surrounding spaces removed,
              or an empty list if input is empty.

    Raises:
        TypeError: If 'lines' is not a list of strings (enforced by the decorator).
    """
        
    if not lines:
        return []

    return [lines[0].strip(" ")]


@only_str_in_list
def clean_data(lines: list) -> list:

    """
    Cleans a list of lines by removing duplicates and trimming leading/trailing spaces.
    The first line is assumed to be a header and is excluded from the result.

    Args:
        lines (list): A list of strings representing lines from a file.

    Returns:
        list: A cleaned list of lines (excluding the header), with duplicates removed 
              and only surrounding spaces stripped (newlines are preserved).

    Raises:
        TypeError: If 'lines' is not a list of strings (enforced by the decorator).
    """

    return [line.strip(" ") for line in set(lines[1:])]


def filter_data(lines: list, header: list) -> list:

    """
    Removes lines from the list that do not have the same number of comma-separated
    fields as the header.

    Args:
        lines (list): A list of strings, each representing a line of data.
        header (list): A list containing the header line (as a single string).

    Returns:
        list: A new list with only complete data lines (excluding the header).

    Raises:
        TypeError: If either 'lines' or 'header' is not a list.
    """

    if not isinstance(lines, list):
        raise TypeError(f"'data' must be a list, got {type(lines).__name__}")
    if not isinstance(header, list):
        raise TypeError(f"'header' must be a list, got {type(header).__name__}")

    header_line = header[0]
    header_fields = header_line.split(",")
    new_lines = []

    for line in lines:
        fields = line.split(",")
        if len(fields) == len(header_fields) and line != header_line:
            new_lines.append(line)

    return new_lines