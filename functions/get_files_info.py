from requests.packages import target
import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory):
    working_directory = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(working_directory, directory))
    valid_target_directory = (
        os.path.commonpath([working_directory, target_directory]) == working_directory
    )
    if directory == ".":
        result_string = "Result for current directory:\n"
    else:
        result_string = f"Result for '{directory}' directory:\n"

    if not valid_target_directory:
        return f'{result_string}    Error: cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_directory):
        return f'   Error: "{result_string}{directory}" is not a directory'

    directory_list = os.listdir(target_directory)

    for f in directory_list:
        f_path = os.path.join(target_directory, f)
        try:
            result_string = (
                result_string
                + f"  - {f}: {os.path.getsize(f_path)}, is_dir={os.path.isdir(f_path)}\n"
            )
        except Exception as error:
            return f"{result_string}    Error: {error}"
    return result_string
