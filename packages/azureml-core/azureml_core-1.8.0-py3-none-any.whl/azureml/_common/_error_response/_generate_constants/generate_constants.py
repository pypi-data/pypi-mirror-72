# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import getopt
import json
import os
import sys

ERROR_CODE_JSON_FILE_PATH = "error_codes.json"
ERROR_CODE_CONSTANTS_FILE_PATH = r"..\_error_response_constants.py"
HEADER_MESSAGE = \
    "# ---------------------------------------------------------\n" \
    "# Copyright (c) Microsoft Corporation. All rights reserved.\n" \
    "# ---------------------------------------------------------\n\n" \
    "r\"\"\"\nDo not modify; this file is autogenerated by azureml-core\\scripts\\generate_constants.py.\n\n" \
    "To add error codes, please refer to error_handling\\readme.md in the Vienna/specs repository.\n\"\"\"\n\n\n"


def recurse_code(errors_list, parent_codes=[]):
    """
    Given a list of error codes, recursively creates a a full error hierarchy for each error.
    :param errors_list: list of json hierarchies of inner errors
    :param parent_codes: Parent error codes that have already been flattened
    :return: list(list(str)) where each element of the outer list is an error code, and the inner list is the
    hierarchy in order of descending granularity.
    """
    if errors_list is None:
        return []
    error_hierarchies = {}
    for inner_error in errors_list:
        code = inner_error.get('error_code', None)
        if code is None:
            continue
        this_code = [code] + parent_codes
        new_inner_errors = inner_error.get("innererrors", [])
        error_hierarchies[this_code[0]] = {
            "description": inner_error.get("_description"), "codes": this_code}
        error_hierarchies.update(recurse_code(new_inner_errors, this_code))

    return error_hierarchies


def write_constants(input_path=None, output_path=None) -> bool:
    """
    Create a python module with string constants for every error code as defined in the input JSON file.

    :param input_path: File path for the input json file containing error codes
    :param output_path: Output for the python module containing error code constants
    :return:
    """
    print(f"Generating error code constants at: {output_path}")
    with open(input_path, "r") as error_codes_file:
        error_codes_string = error_codes_file.read()
        error_codes = json.loads(error_codes_string)
        all_codes = error_codes['innererrors']
        all_codes_parsed = recurse_code(all_codes)

        with open(output_path, "w") as constants:
            constants.write(HEADER_MESSAGE)
            constants.write(
                "class ErrorCodes:\n    \"\"\"Constants for error codes.\"\"\"\n\n")
            string_objects = ""
            hierarchy_objects = ""
            tab = "    "
            linelength = 119
            for _, error_dict in all_codes_parsed.items():
                error = error_dict["codes"]
                description = error_dict["description"]
                suffix = "_ERROR"
                error_name = error[0]
                if error[0].endswith("Error"):
                    error_name = error[0][:-5]
                if description is not None:
                    sentences = []
                    if len(tab + tab + description) > linelength:
                        words = description.split(" ")
                        buffer = ""
                        for word in words:
                            if (len(tab * 2 + buffer + word)) > linelength:
                                sentences.append(buffer)
                                buffer = word
                            else:
                                buffer += (" " + word)
                        if buffer != "":
                            sentences.append(buffer)
                    else:
                        sentences = [description]
                    for sentence in sentences:
                        string_objects += tab + "# " + sentence + "\n"
                string_objects += tab + error_name.upper() + suffix + " = \"" + \
                    error[0] + "\"\n\n"

                hierarchy_object = tab + error_name.upper() + suffix + " = [\n"
                for level in error:
                    suffix = "_ERROR"
                    if level.lower().endswith("error"):
                        level = level[:-5]
                    hierarchy_object += tab + tab + "ErrorCodes." + level.upper() + suffix + ",\n"
                hierarchy_object += tab + "]\n"
                hierarchy_objects += hierarchy_object

            constants.write(string_objects)
            constants.write("\n")
            constants.write(
                "class ErrorHierarchy:\n    \"\"\"Constants containing full error hierarchies.\"\"\"\n\n")
            constants.write(hierarchy_objects)
            return True


if __name__ == '__main__':
    input_path = ERROR_CODE_JSON_FILE_PATH
    output_path = ERROR_CODE_CONSTANTS_FILE_PATH
    argv = sys.argv[1:]
    opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    for opt, arg in opts:
        if opt == "-h":
            print(f"Generates the {input_path} file.")
            print(
                f"{os.path.basename(__file__)} {{-i <input json>}} {{-o <output python script>}}")
            sys.exit(2)
        if opt == "-i":
            input_path = arg
        if opt == "-o":
            output_path = arg

    write_constants(input_path, output_path)
