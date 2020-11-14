from sys import argv
from os import path
from glob import glob
import re

def pretty_list(items):
	return "\n\t" + "\n\t".join(items)

def main():
    
    if len(argv) == 1 or not path.isdir(argv[1]):
        print("Please pass a valid directory")
        return

    source_path = argv[1].rstrip('/') + "/**/*.py"
    print(f"Reading: {source_path}")

    modules = []

    for f in glob(source_path, recursive=True):
        with open(f) as source_code:
            
            text = source_code.read()
            
            modules.extend(re.findall("^import (\w+)$", text, re.M))
            modules.extend(re.findall("^from (\w+) import \w+$", text, re.M))
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
