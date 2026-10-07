import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        # Set up & validate path
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_file = os.path.commonpath([abs_path, target_file]) == abs_path
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        # Writing the file
        os.makedirs(abs_path, exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Overwrite a file or write into a file in the working directory, creating all directories on the path to file if not exist",
        "parameters": {
            "type": "object",
            "required": [
                "file_path",
                "content",
            ],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to the file we want to write into, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write into the file",
                },
            },
        },
    },
}
