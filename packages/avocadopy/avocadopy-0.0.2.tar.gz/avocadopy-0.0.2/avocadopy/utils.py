import logging
import subprocess

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s|%(levelname)s|%(message)s')


def shell_run(cmd, check=True):
    """Run a command in shell.

    Args:
        cmd (str): A command
        check (bool, optional): check of subprocess.run(). Defaults to True.
    """
    logging.info(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=check)


def unique(input_list):
    """Make a unique list from input.

    Args:
        input_list (list): A list to remove duplication.

    Returns:
        list: A list with no duplication.
    """
    # insert the list to the set
    list_set = set(input_list)
    # convert the set to the list
    unique_list = (list(list_set))
    return unique_list


def create_file(filename):
    """Create an empty file with name of 'filename'

    Args:
        filename (str): File name.
    """
    with open(filename, 'w') as f:
        pass
