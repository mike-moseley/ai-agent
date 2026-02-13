import os

# TODO: config file for globals
MAX_CHARS = 10000

def get_file_content(working_directory, file_path):

    working_directory = os.path.abspath(working_directory)
    target = os.path.normpath(os.path.join(working_directory, file_path))
    valid_target = (
        os.path.commonpath([working_directory, target]) == working_directory
    )
    if not valid_target:
        return f'   Error: cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target):
        return f'   Error: File not found or is not a regular file: "{file_path}"'

    try:
        f = open(target)
        content = f.read(MAX_CHARS)
        if f.read(1):
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except Exception as error:
        return f'   Error: {error}'

    return content
