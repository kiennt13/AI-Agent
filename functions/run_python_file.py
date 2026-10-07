import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        # Set up & validate path
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_file = os.path.commonpath([abs_path, target_file]) == abs_path
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        # Set up the python command
        command = ["python", target_file]
        if args is not None:
            command.extend(args)
        command_output = subprocess.run(command, capture_output=True, text=True, timeout=30)
        string_output = []
        if command_output.returncode != 0:
            string_output.append(f"Process exited with code {command_output.returncode}")
        if command_output.stdout is None and command_output.stderr is None:
            string_output.append("No output produced")
        if command_output.stdout is not None:
            string_output.append(f"STDOUT: {command_output.stdout}")
        if command_output.stderr is not None:
            string_output.append(f"STDERR: {command_output.stderr}")
        return "\n".join(string_output)
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run a Python file and return its stdout and stderr.",
        "parameters": {
            "type": "object",
            "required": [
                "file_path",
            ],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to the python file to execute, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional command-line arguments for the Python file.",
                },
            },
        },
    },
}
