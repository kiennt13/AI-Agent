import os
from config import *


def get_file_content(working_directory: str, file_path: str) -> str:
    # Set up and validate paths
    try:
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_file = os.path.commonpath([abs_path, target_file]) == abs_path
        if not valid_target_file:
            return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
        if not os.path.isfile(target_file):
            return f"Error: File not found or is not a regular file: \"{file_path}\""
    except Exception as e:
        return f"Error: {e}"
    # Reading the file
    try:
        with open(target_file, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f"[...File \"{file_path}\" truncated at {MAX_CHARS} characters]"
        return content
    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Print the content of a file in the working directory, printing only MAX_CHARS characters, if the content of the file is longer than MAX_CHARS, add a string explaining that the result is truncated",
        "parameters": {
            "type": "object",
            "required": [
                 "file_path",
             ],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file path to the file we want to print its content, relative to the working directory (default is the working directory itself)"
                },
            },
        },
    },
}
