import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path, args=None):
    absolute_working = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not target_file.startswith(absolute_working):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_file):
        return f'Error: File "{file_path}" not found.'

    if not target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        commands = ["python3", target_file]
        if args:
            commands.extend(args)
        completed = subprocess.run(
            commands, capture_output=True, timeout=30, text=True, cwd=absolute_working
        )
        if not completed:
            return "No output produced."
        output = f"STDOUT: {completed.stdout}\nSTDERR: {completed.stderr}\n"
        if completed.returncode != 0:
            output += f"Process exited with code {completed.returncode}\n"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="""Checks if target file exists and if it is a python file
        it runs it with the arguments passed""",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="""target file to be run""",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="""Arguments used to run the function in a python file""",
            ),
        },
    ),
)
