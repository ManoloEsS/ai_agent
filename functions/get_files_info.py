import os

from google.genai import types


from typing import Optional


def get_files_info(working_directory: str, directory: Optional[str] = None) -> str:
    """List files and directories with their sizes in the specified directory.

    Args:
        working_directory: The base working directory path.
        directory: Optional relative path to a subdirectory. If not provided,
            lists files in the working directory itself.

    Returns:
        A string containing file information (name, size, is_dir status)
        for each item in the directory, or an error message.
    """
    absolute_working = os.path.abspath(working_directory)
    target_dir = absolute_working

    if directory:
        target_dir = os.path.abspath(os.path.join(working_directory, directory))
    if not target_dir.startswith(absolute_working):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        files_info = []
        for filename in os.listdir(target_dir):
            filepath = os.path.join(target_dir, filename)
            file_size = 0
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)
            files_info.append(
                f"- {filename}: file_size= {file_size} bytes, is_dir={is_dir}"
            )

        return "/n".join(files_info)

    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="""Lists files in the specified directory 
            along with their sizes and wether they are a directory,
            constrained to the working directory.""",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="""The directory to list files from,
                        relative to the working directory. If not
                        provided, lists files in the working directory itself.""",
            ),
        },
    ),
)
