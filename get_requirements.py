from sys import argv
from os import path
from glob import glob
import re
IGNORE_ENVIRONMENTS = ['env', 'venv']


def pretty_list(items):
    return "\n\t" + "\n\t".join(items)


def main():

    # General Clean-up: Remove quotes and add a trailing backslash
    base = argv[1].rstrip('/').replace('"', '').replace("'", '') + '/'

    if len(base) <= 1 or not path.isdir(base):
        print("Please pass a valid directory")
        return

    source_path = base + "**/*.py"
    
    print(f"Reading: {source_path}")

    modules = []

    # Define a quick filter for filtering environments
    def environment_filter(path_string):
        return not any(path_string.startswith(path.join(base, e)) for e in IGNORE_ENVIRONMENTS)

    for f in filter(environment_filter, glob(source_path, recursive=True)):
        with open(f) as source_code:
            
            text = source_code.read()
            
            modules.extend(re.findall(r"^import (\w+)$", text, re.M))
            modules.extend(re.findall(r"^from (\w+) import \w+$", text, re.M))
            # print(f"Reading: {f} Modules: {modules}")

    modules = list(set(modules))
    installed, not_installed = [], []

    for x in modules:
        try:
            __import__(x)
        except:
            not_installed.append(x)
        else:
            installed.append(x)
        
    print(not_installed)
    print("The project uses following modules: ")
    print(pretty_list(modules))

    print(f"These are installed: {pretty_list(installed)}")
    print(f"These are not installed: {pretty_list(not_installed)}")


if __name__ == '__main__':
    main()
