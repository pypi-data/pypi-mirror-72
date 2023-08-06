"""
Template for the agpipeline_templates files
"""

import os
import sys
import laspy
import numpy as np
import agpipeline_templates.algorithm as algorithm
import gdal


def get_variables_header_fields() -> str:
    """Returns a string representing the variable header fields
    Return:
        Returns a string representing the variables' header fields
    """
    variables = algorithm.VARIABLE_NAMES.split(',')
    labels = algorithm.VARIABLE_LABELS.split(',')
    labels_len = len(labels)
    units = algorithm.VARIABLE_UNITS.split(',')
    units_len = len(units)

    if labels_len != len(variables):
        sys.stderr.write("The number of defined labels doesn't match the number of defined variables")
        sys.stderr.write("  continuing processing")
    if units_len != len(variables):
        sys.stderr.write("The number of defined units doesn't match the number of defined variables")
        sys.stderr.write("  continuing processing")

    headers = ''
    for idx, variable_name in enumerate(variables):
        variable_header = variable_name
        if idx < labels_len:
            variable_header += ' - %s' % labels[idx]
        if idx < units_len:
            variable_header += ' (%s)' % units[idx]
        headers += variable_header + ','

    return headers


def print_usage(args, file):
    """Displays information on how to use this script
    """
    print("length of arguments: " + str(len(args)))
    print("arguments: " + args[0])
    print()
    if len(args):
        our_name = os.path.basename(args[0])
    else:
        our_name = os.path.basename(file)
    print(our_name + " <folder>|<filename> ...")
    print("    folder:   path to folder containing files to process")
    print("    filename: path to a file to process")
    print("")
    print("  One or more folders and/or filenames can be used")
    print("  Only files at the top level of a folder are processed")


def check_arguments(args, file):
    """Checks that we have script argument parameters that appear valid
    """

    if len(args) < 2:
        sys.stderr.write("One or more paths to images need to be specified on the command line\n")
        print_usage(args, file)
        return False

    # Check that the paths exist.
    no_errors = True
    for idx in range(1, len(args)):
        if not os.path.exists(args[idx]):
            print("The following path doesn't exist: " + args[idx])
            no_errors = False

    if not no_errors:
        sys.stderr.write("Please correct any problems and try again\n")
    return no_errors


def check_configuration():
    """Checks if the configuration is setup properly for agpipeline_templates
    """
    if len(algorithm.VARIABLE_NAMES) == 0:
        sys.stderr.write("Variable names configuration variable is not defined yet. Please define and try again")
        sys.stderr.write("    Update configuration.py and set VALUE_NAMES variable with your variable names")
        return False

    return True


def run_test(filename, mode):
    """Runs the extractor code using pixels from the file
    Args:
        filename(str): Path to image file
        mode(int): Denotes file-opening type (laspy vs gdal)
    Return:
        The result of calling the extractor's calculate() method
    Notes:
        Assumes the path passed in is valid. An error is reported if
        the file is not an image file.
    """

    # Check for unsupported types
    try:
        if mode == 1:
            open_file = laspy.file.File(filename, mode="r")
        elif mode == 2:
            open_file = gdal.Open(filename)
        if open_file:
            # Get the pixels and call the calculation
            if mode == 1:
                pix = np.vstack([open_file.X, open_file.Y, open_file.Z])
                calc_val = algorithm.calculate(pix)
            elif mode == 2:
                pix = np.array(open_file.ReadAsArray())
                calc_val = algorithm.calculate(np.rollaxis(pix, 0, 3))
            if isinstance(calc_val, set):
                raise RuntimeError("A 'set' type of data was returned and isn't supported.  Please use a list or a "
                                   "tuple instead")

            # Perform any type conversions to a printable string
            if isinstance(calc_val, str):
                print_val = calc_val
            else:
                # Check if the return is iterable and comma separate the values if it is
                try:
                    _ = iter(calc_val)
                    print_val = ",".join(map(str, calc_val))
                except Exception:
                    print_val = str(calc_val)
            print(filename + "," + print_val)
    except Exception as ex:
        sys.stderr.write("Exception caught: " + str(ex) + "\n")
        sys.stderr.write("    File: " + filename + "\n")


def process_files(args, mode, supported_exts):
    """Processes the command line file/folder arguments
    """
    if len(args):
        print("Filename," + algorithm.VARIABLE_NAMES)
        for idx in range(1, len(args)):
            cur_path = args[idx]
            if not os.path.isdir(cur_path):
                run_test(cur_path)
            else:
                allfiles = [os.path.join(cur_path, fn) for fn in os.listdir(cur_path) if
                            os.path.isfile(os.path.join(cur_path, fn))]
                for one_file in allfiles:
                    ext = os.path.splitext(one_file)[1]
                    if ext and ext in supported_exts:
                        run_test(one_file, mode)
                    else:
                        print("File " + one_file + " does not have a supported extention.")


if __name__ == "__main__":
    if check_arguments() and check_configuration():
        process_files()
