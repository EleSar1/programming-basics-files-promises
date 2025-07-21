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
    except IOError:
        print(f"head: cannot open '{filename}' for reading: No such file or directory.")
    except FileNotFoundError:
        return []
    except PermissionError:
        print(f"head: cannot open '{filename}' for reading: Permission denied.")
        return []
    except Exception as e:
        print(f"head: error reading '{filename}': {e}")
        return []


def read_n_lines(lines: list, n_lines: int=10):
    
    """
    Yields the first `n_lines` elements from a list of lines.

    Parameters:
        lines (list): A list of strings, typically lines from a file.
        n_lines (int, optional): The number of lines to yield. Defaults to 10.

    Yields:
        str: The next line from the list, up to `n_lines` lines.

    Raises:
        TypeError: If 'lines' is not a list or 'n_lines' is not an integer.
    """

    if not isinstance(lines, list):
        raise TypeError("Expected 'lines' to be a list, got a different type.")
    if not isinstance(n_lines, int):
        raise TypeError("Expected 'n_lines' to be an integer, got a different type.")
    

    if len(lines) < n_lines:
        n_lines = len(lines)

    if lines:
        for i in range(n_lines):
            yield lines[i]


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


def simulate_head(filenames: list, n: int=10, verbose: bool=False) -> None:

    """
    Simulates the behavior of the Unix 'head' command by printing the first `n` lines of each file.

    Parameters:
        filenames (list): A list of filenames (strings) to read and display lines from.
        n (int, optional): The number of lines to display from each file. Defaults to 10.
        verbose (bool, optional): If True, always display the filename header.
                                  If False, display it only when multiple files are provided.

    Returns:
        None

    Raises:
        TypeError: If 'filenames' is not a list, 'n' is not an integer, or 'verbose' is not a boolean.
    """

    if not isinstance(filenames, list):
        raise TypeError("Expected 'filenames' to be a list, got a different type.")
    if not isinstance(n, int):
        raise TypeError("Expected 'n' to be an integer, got a different type.")
    if not isinstance(verbose, bool):
        raise TypeError("Expected 'verbose' to be a bool, got a different type.")

    multiple_files = len(filenames) > 1

    for file in filenames:
        lines = save_lines(file)
        if not lines:
            return 
            
        if verbose or multiple_files:
            print(show_filename(file))

        for line in read_n_lines(lines, n):
            print(line, end="")

        if multiple_files:
            print()


def handle_user_input(command: str) -> tuple[list, int, bool] | None:

    """
    Parses a command string simulating the 'head' command and extracts filenames,
    the number of lines to display, and the verbosity option.

    Parameters:
        command (str): A string representing the user command 
                       (e.g., "head -n 5 -v file1.txt file2.txt").

    Returns:
        tuple: A tuple (filenames: list, n: int, verbose: bool) if parsing is successful.
        None: If no filenames are provided or if the command is invalid or improperly formatted.

    Raises:
        TypeError: If 'command' is not a string.
    """

    if not isinstance(command, str):
        raise TypeError("Expected 'command' to be a string, got a different type.")
    
    tokens = command.split()
    filenames = []
    verbose = False
    n = 10

    if tokens[0] != "head":
        print(f"command not found: {tokens[0]}")
        return None

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == 'head':
            i += 1
        elif token == '-n':
            i += 1
            if i < len(tokens):
                try:
                    n = int(tokens[i])
                except ValueError:
                    print("Invalid number after -n")
                    return None
                i += 1
            else:
                print("Option -n requires an argument")
                return None
        elif token == '-v':
            verbose = True
            i += 1
        else:
            filenames.append(token)
            i += 1

    if not filenames:
        print("No input files specified.")
        return None

    return filenames, n, verbose


def main() -> None:

    print("Command head simulator -> ")
    command = input().lower().strip()

    filenames, n, verbose = handle_user_input(command)
    simulate_head(filenames, n=n, verbose=verbose)


if __name__ == "__main__":
    main()