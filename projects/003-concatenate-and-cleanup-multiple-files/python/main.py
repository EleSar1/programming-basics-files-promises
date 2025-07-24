from functools import wraps
import os


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



def load_lines(file_path: str) -> list:

    """
    Reads all lines from a text file and returns them as a list of strings.

    Args:
        file_path (str): Path to the file to read.

    Returns:
        lines (list): A list of lines from the file. Returns an empty list when raise an error.

    Raises:
        TypeError: If 'file_path' is not a string.
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be accessed due to permission issues.
    """

    if not isinstance(file_path, str):
        raise TypeError(f"Expected str for filename, got {type(file_path).__name__}.")
    
    try:
        with open(file_path, mode="r") as f:
            lines = f.readlines()
            return lines
    except (FileNotFoundError, PermissionError) as e:
        raise e

    return []


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


def delete_incomplete_data(lines: list, header: list) -> list:

    """
    Removes lines from the list that do not have the same number of comma-separated
    fields as the header.

    Args:
        lines (list): A list of strings, each representing a line of data.
        header (list): A list containing the header line (as a single string).

    Returns:
        list: The same list with incomplete lines removed (modified in-place).

    Raises:
        TypeError: If either 'lines' or 'header' is not a list.
    """

    if not isinstance(lines, list):
        raise TypeError(f"'data' must be a list, got {type(lines).__name__}")
    if not isinstance(header, list):
        raise TypeError(f"'header' must be a list, got {type(header).__name__}")

    header_line = " ".join(header)
    header_fields = header_line.split(",")
    i = 0

    while i < len(lines):
        lines_details = lines[i].split(",")
        if len(lines_details) != len(header_fields):
            del lines[i]
        else:
            i += 1

    return lines


def merge_data(filename: str, header: list, lines_to_add: list) -> None:

    """
    Appends the given lines to the specified file. If the file is empty,
    the header is written first.

    Args:
        filename (str): Path to the file to be written to.
        header (list): List containing header line(s) to be written if file is empty.
        lines_to_add (list): List of string lines to append to the file.

    Raises:
        TypeError: If any input is of the wrong type.
        FileNotFoundError: If the target file does not exist.
        PermissionError: If file cannot be accessed due to permission restrictions.
    """

    if not isinstance(lines_to_add, list):
        raise TypeError(f"'lines_to_add' must be a list, got {type(lines_to_add).__name__}.")
    if not isinstance(header, list):
        raise TypeError(f"'header' must be a list, got {type(header).__name__}.")
    if not isinstance(filename, str):
        raise TypeError(f"Expected str for filename, got {type(filename).__name__}.")

    if not os.path.exists(filename):
        raise FileNotFoundError(f"Can't open {filename}: no such file or directory.")
    
    try:
        if os.path.getsize(filename) == 0:
            with open(filename, mode="a") as f:
                f.writelines(header)
        
        with open(filename, mode="a") as f:
            f.writelines(lines_to_add)

    except PermissionError as e:
            raise e


def main() -> None:
    filenames = ["products_files/products_1.txt", "products_files/products_2.txt", "products_files/products_3.txt"]
    concatenated = concatenate_data(filenames)
    header = save_header(concatenated)
    cleaned = clean_data(concatenated)
    print(cleaned)
    final_data = delete_incomplete_data(cleaned, header)    

    merge_data("combined_products.txt", header, final_data)


if __name__ == "__main__":
    main()