from functions.get_files_info import get_files_info


print("Result for current directory")
print(get_files_info("calculator", "."))

dir_name = ["pkg", "/bin", "../"]
for dir in dir_name:
    print(f"Result for '{dir}' directory")
    print(get_files_info("calculator", dir))
