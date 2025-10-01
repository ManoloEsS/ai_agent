import os

from google.genai import types


def write_file(working_directory: str, file_path: str, content: str) -> str:
    """Write content to a file, creating it and parent directories if needed.
    
    Args:
        working_directory: The base working directory path.
        file_path: Relative path to the target file to write.
        content: The content to write to the file.
    
    Returns:
        A success message with the number of characters written,
        or an error message if the write operation fails.
    """
    absolute_working = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(absolute_working):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_file):
        try:
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"

    if os.path.exists(target_file) and os.path.isdir(target_file):
        return f'Error: "{target_file}" is a directory, not a file'

    try:
        with open(target_file, "w+") as f:
            f.write(content)
        return f'Succesfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="""Checks if target file exists and either writes on it 
        or creates it.""",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="""target file to be created and written""",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="""Content to be written into the target file""",
            ),
        },
    ),
)
