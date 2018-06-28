import os, re


def to_abs_path(path):
    """
    transforms a possibly relative path into an absolute path.
    :param path: string
    :raises IOError if the path (either absolute or relative) points to an invalid file
    :return: the absolute path equivalent of the input parameter
    """
    if os.path.isabs(path):
        absolute_path = path
    else:
        absolute_path = os.path.abspath(path)

    if not os.path.isfile(absolute_path):
        raise IOError("file not found: {}".format(path))

    return absolute_path


def get_files_matching(absolute_path_to_directory, pattern):
    """

    Searches the given ABSOLUTE directory path for files whose names match the given regexp pattern

    :param absolute_path_to_directory: absolute path to directory to be searched
    :param pattern: a string that can be interpreted as a ptyhon regular exception
    :return: list of absolute paths to files (possibly empty) matching the criteria
    """

    # we require absolute paths to avoid confusions w.r.t. paths relative to the CWD and
    # paths relative to this file's location.
    if not os.path.isabs(absolute_path_to_directory):
        raise IOError("invalid absolute path given: {}".format(absolute_path_to_directory))

    if not os.path.isdir(absolute_path_to_directory):
        raise IOError("invalid directory path given: {}".format(absolute_path_to_directory))

    return [absolute_path_to_directory + "/" + file for file in os.listdir(absolute_path_to_directory) if
            re.match(pattern, file)]
