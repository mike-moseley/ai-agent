import os

def write_file(working_directory, file_path, content):
    working_directory = os.path.abspath(working_directory)
    target = os.path.normpath(os.path.join(working_directory, file_path))
    valid_target = (
        os.path.commonpath([working_directory, target]) == working_directory
    )
    if not valid_target:
        return f'   Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target):
        return f'   Error: Cannot write to "{file_path}" as it is a directory'

    try:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target,mode="w") as f:
            f.write(content)
    except Exception as error:
        return f"   Error: {error}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
