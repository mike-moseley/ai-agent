from subprocess import STDOUT
import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a python file in specified directory relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "args": types.Schema(
                    type=types.Type.STRING,
                    description="Arguments to be passed to the python code"
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path the file is located in, relative to the working directory, or . (default is the working directory itself)",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    working_directory = os.path.abspath(working_directory)
    target = os.path.normpath(os.path.join(working_directory, file_path))
    valid_target = (
        os.path.commonpath([working_directory, target]) == working_directory
    )
    if not valid_target:
        return f'   Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target):
        return f'   Error: "{file_path}" does not exist or is not a regular file'
    if not file_path.endswith(".py"):
        return f'   Error: "{file_path}" is not a Python file'

    try:
        command = ["python", target]
        if not args == None:
            command.extend(args)

        process = subprocess.run(command, capture_output=True, cwd=working_directory,timeout=30)
    except Exception as error:
        return f'   Error: executing Python file:{error}'

    return_string = f""
    if not process.returncode:
        return_string += f"Process exited with code {process.returncode}\n"
    if process.stdout is None and process.stderr is None:
        return_string += "No output produced\n"
    if not process.stdout is None:
        return_string += f"STDOUT: {process.stdout}"
    if not process.stderr is None:
        return_string += f"STDERR: {process.stderr}"

    return return_string



