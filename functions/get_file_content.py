import os

from google.genai import types

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    """Read and return the contents of a file, with security checks and truncation.
    
    Args:
        working_directory: The base working directory path.
        file_path: Relative path to the target file to read.
    
    Returns:
        The file contents as a string, truncated to MAX_CHARS if necessary,
        or an error message if the file cannot be read.
    """
    absolute_working = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(absolute_working):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: "File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            more = f.read(1)
            if more:
                file_content_string += (
                    f'[...File "{file_path}" truncated at 10000 characters]'
                )
            return file_content_string
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="""Checks if file exists and reads it, returns
        the contents truncated to MAX_CHARS""",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="""Target file to check and read contents from""",
            ),
        },
    ),
)
