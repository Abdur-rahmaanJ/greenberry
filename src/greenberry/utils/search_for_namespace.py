import os

def search_for_namespace(name: str, directory: str):
    dir_tree = os.walk(directory)
    files = ""
    for (root, files, file_paths) in dir_tree:
        for file in file_paths:
            if file == name:
                files.append(file)
    
    return files
    

        