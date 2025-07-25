import os


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