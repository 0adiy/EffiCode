import requests
import json
import argparse
from termcolor import cprint


def ext_to_lang(file_extension):
    # getting file type
    match file_extension:
        case "cpp":
            return "cpp"
        case "c":
            return "c"
        case "py":
            return "python"
        case "java":
            return "java"
        case "js":
            return "javascript"
        case "cs":
            return "csharp"


def get_data(input: str, filename: str) -> dict:
    """
    Retrieves data by sending a POST request to the specified API endpoint.

    Parameters:
        input (str): The input code to be executed.
        filename (str): The name of the file containing the input code.

    Returns:
        dict: The JSON response from the API endpoint.
    """
    url = "https://onecompiler.com/api/code/exec"

    file_extension = filename.split(".")[-1]
    language = ext_to_lang(file_extension)
    request_obj = {
        "properties": {
            "language": language,
            "files": [{"name": filename, "content": input}],
        },
    }

    headers = {
        "content-type": "application/json",
    }
    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(request_obj),
    ).json()

    return response["stdout"], response["stderr"], response["executionTime"]


if __name__ == "__main__":
    # Parsing Args
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="the file to compile")
    args = parser.parse_args()
    filename = args.file

    # reading file
    content = ""
    with open(filename) as f:
        content = f.read()

    # Getting Response
    stdout, stderr, executionTime = get_data(content, filename)

    # Printing
    if stdout:
        print(stdout)
    if stderr:
        cprint(stderr, "red")
    cprint(f"Execution Time : {executionTime}ms", "yellow")
