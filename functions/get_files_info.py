import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    # validate the input/dir path
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, directory))
        valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path
        if not valid_target_dir:
            return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
        elif not os.path.isdir(target_dir):
            return f"Error: \"{directory}\" is not a directory"
    except Exception as e:
        return f"Error: {e}"
    # print descriptions of the file within
    try:
        files_name = os.listdir(target_dir)
        files_description = []
        for file in files_name:
            size = os.path.getsize(target_dir + "/" + file)
            is_dir = os.path.isdir(target_dir + "/" + file)
            file_description = f"- {file}: file_size={size}, is_dir={is_dir}"
            files_description.append(file_description)
        return "\n".join(files_description)
    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
