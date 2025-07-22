def save_lines(filename: str) -> list:

    """
    Reads the contents of a file and returns its lines as a list.

    Parameters:
        filename (str): The path to the file to be read.

    Returns:
        list: A list of strings, each representing a line from the file.
              Returns an empty list if the file is not found or cannot be accessed.
              
    Raises:
        TypeError: If 'filename' is not a string.
    """

    if not isinstance(filename, str):
        raise TypeError("Expected 'filename' to be a string, got a different type.")

    try:
        with open(filename, mode="r") as f:
            lines = f.readlines()
            return lines
    except FileNotFoundError:
        print(f"head: cannot open '{filename}' for reading: No such file or directory.")
        return []
    except PermissionError:
        print(f"head: cannot open '{filename}' for reading: Permission denied.")
        return []
    except Exception as e:
        print(f"head: error reading '{filename}': {e}")
        return []
    
    
def read_n_lines(lines: list, n_lines: int=10, plus_sign: bool=False):
    
    """
    Yields lines from a list based on tail-like behavior.

    If plus_sign is False, yields the last 'n_lines' lines (like `tail -n N`).
    If plus_sign is True, yields lines starting from the 'n_lines'-th line (like `tail -n +N`).

    Args:
        lines (list): List of strings (e.g., file lines).
        n_lines (int): Line index or count, depending on 'plus_sign'.
        plus_sign (bool): Determines line selection behavior.

    Yields:
        str: Line from the list.

    Raises:
        TypeError: If inputs are not of the expected types.
    """

    if not isinstance(lines, list):
        raise TypeError("Expected 'lines' to be a list, got a different type.")
    if not isinstance(n_lines, int):
        raise TypeError("Expected 'n_lines' to be an integer, got a different type.")
    if not isinstance(plus_sign, bool):
        raise TypeError("Expected 'plus_sign' to be a bool, got a different type.")

    if len(lines) < n_lines:
        n_lines = len(lines)

    if plus_sign:
        for line in lines[n_lines - 1:]:
            yield line
    else:
        for line in lines[-n_lines:]:
            yield line


def show_filename(filename: str) -> str:

    """
    Formats and returns the given filename with decorative markers.

    Parameters:
        filename (str): The name of the file to format.

    Returns:
        str: The formatted string in the form "====> filename <====".

    Raises:
        TypeError: If 'filename' is not a string.
    """

    if not isinstance(filename, str):
        raise TypeError("Expected 'filename' to be a string, got a different type.")

    return f"====> {filename} <===="


def simulate_tail(filenames: list, n: int=10, plus_sign: bool=False) -> None:

    """
    Simulates the behavior of the Unix 'tail' command by printing the last 'n' lines or from the 'n' lines of each file.

    Parameters:
        filenames (list): A list of filenames (strings) to read and display lines from.
        n (int, optional): The number of lines to display from each file. Defaults to 10.
        plus_sign (bool, optional): If True, starts output from the 'n'-th line. If False, shows the last 'n' lines.
                                    Defaults to False.

    Returns:
        None

    Raises:
        TypeError: If 'filenames' is not a list or 'n' is not an integer.
    """

    if not isinstance(filenames, list):
        raise TypeError("Expected 'filenames' to be a list, got a different type.")
    if not isinstance(n, int):
        raise TypeError("Expected 'n' to be an integer, got a different type.")

    multiple_files = len(filenames) > 1

    for file in filenames:
        lines = save_lines(file)
        if not lines:
            return 
            
        if multiple_files:
            print(show_filename(file))

        for line in read_n_lines(lines, n, plus_sign):
            print(line, end="")

        if multiple_files:
            print()


def handle_user_input(command: str) -> tuple[list, int, bool] | bool:

    """
    Parses a command string simulating the 'tail' command and extracts filenames and options.

    Supports:
    - Standard syntax: `tail filename`
    - Line count option: `tail -n N filename`
    - Starting from line N: `tail -n +N filename` or `tail +N filename`

    Args:
        command (str): The full command string entered by the user.

    Returns:
        tuple[list, int, bool] | bool:
            If parsing is successful, returns a tuple containing:
                - filenames (list of str): List of filenames provided.
                - n (int): Number of lines or starting line number.
                - plus_sign (bool): True if using +N syntax, otherwise False.
            Returns False if there is a parsing error.

    Raises:
        TypeError: if 'command' parameter is not a string.
        Prints error messages and returns False for invalid input.
    """

    if not isinstance(command, str):
        raise TypeError("Expected string for 'command', got a different type.")

    tokens = command.split()
    filenames = []
    n = 10
    plus_sign = False

    if tokens[0] != "tail":
        print(f"command not found: {tokens[0]}")
        return False

    i=0
    while i < len(tokens):
        
        token = tokens[i]
        if token == 'tail':
            i += 1
        
        elif token == '-n':
            i += 1
            if i < len(tokens):
                try:
                    n = int(tokens[i])
                    i += 1
                    if n < 1:
                        print("The number of lines to read must be positive.")
                        return False
                except ValueError:
                    print("Invalid number after -n.")
                    return False
            else:
                print("Option -n requires an argument.")

        elif token[0] == '+':
            plus_sign = True
            try: 
                n = int(token[1:])
                i += 1
            except ValueError:
                print("Number required after '+' sign.")
                return False

        else:
            filenames.append(token)
            i+=1

    if not filenames:
        print("No input files specified.")
        return False

    return filenames, n, plus_sign


def main():

    print("Tail command simulator ->")
    command = input().lower().strip()

    result = handle_user_input(command)
    if result:
        filenames, n, plus_sign = result
        simulate_tail(filenames, n, plus_sign)
    else:
        print("Something went wrong.")


if __name__ == "__main__":
    main()