import os


def get_files_info(working_directory, directory):
    if not os.path.isdir(directory):
        raise Exception(f'Error: "{directory}" is not a directory')

    working_directory = os.path.abspath(working_directory)
    target_directory = os.path.normpath(os.path.join(working_directory, directory))
    valid_target_directory = (
        os.path.commonpath([working_directory, target_directory]) == working_directory
    )

    if not valid_target_directory:
        raise Exception(
            f'Error: cannot list "{directory}" as it is outside the permitted working directory'
        )

    directory_list = os.listdir(target_directory)

    result_string = f"Result for {directory}\n"
    for f in directory_list:
        try:
            result_string = (
                result_string
                + f"  - {f}: {os.path.getsize(f)}, is_dir={os.path.isdir(f)}"
            )
        except Exception as error:
            return f"Error: {error}"
