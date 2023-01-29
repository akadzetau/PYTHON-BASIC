"""
Read files from ./files and extract values from them.
Write one file with all values separated by commas.

Example:
    Input:

    file_1.txt (content: "23")
    file_2.txt (content: "78")
    file_3.txt (content: "3")

    Output:

    result.txt(content: "23, 78, 3")
"""
import os


def read_files(path: str) -> list:
    files = os.listdir(path)
    files.sort(key=lambda f: int(f.split('.')[0].split('_')[1]))
    result = []

    for file in files:
        with open(f"{path}/{file}", 'r') as f:
            for line in f:
                result.append(line)

    return result


def write_file(file: str, file_content: str) -> None:
    with open(file, 'w') as f:
        f.write(file_content)


if __name__ == "__main__":
    content = read_files("files")
    write_file("result.txt", ", ".join(content))
