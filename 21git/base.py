import os
from . import data
from collections import namedtuple
import itertools
import operator

def write_tree(directory: str = ".") -> bytes:
    # Recursively build a tree object, hashing files and subdirectories
    entries = []
    with os.scandir(directory) as dir_tree:
        for entry in dir_tree:
            if entry.is_file(follow_symlinks=False):
                try:
                    # Hash file contents
                    type_ = "blob"
                    with open(entry.path, 'rb') as file:
                        oid = data.hash_object(file.read())
                except FileNotFoundError:
                    print(f"File:{entry.path} Not Found")
                    # Handle the case where the file was deleted or moved after the check
                    continue
            elif is_ignored(entry.path):
                # Skip ignored directories
                continue
            elif not entry.name.startswith('.') and entry.is_dir(follow_symlinks=False):
                try:
                    # Recursively process subdirectories
                    type_ = "tree"
                    oid = write_tree(entry.path)
                except FileNotFoundError:
                    print(f"Directory:{entry.path} Not Found")
                    # Handle the case where the file was deleted or moved after the check
                    continue
            else:
                continue
            
            entries.append((entry.name, oid, type_))
    
    # Create tree object from sorted entries
    tree = ''.join(f"{type_} {oid} {name}\n" for name, oid, type_ in sorted(entries))
    return data.hash_object(tree.encode(), "tree")


def _iter_tree_entries(oid_parameter:str):
    # Return early if oid_parameter is None or empty
    if not oid_parameter:
        return
    # Retrieve the tree object and decode it
    tree = data.get_object(oid_parameter, "tree")
    for entry in tree.decode().splitlines():
        # Split each entry into type, oid, and name
        type_, oid, name = entry.split(" ", 2)
        yield type_, oid, name  # Yield parsed entry for iteration


def get_tree(oid_parameter: str, base_path: str = "") -> dict:
    result = {}
    for type_, oid, name in _iter_tree_entries(oid_parameter):
        # Validate entry names to avoid invalid characters or reserved names
        if '/' in name:
            raise ValueError(f"Invalid tree entry name '{name}': must not contain '/'")
        if name in ('..', '.'):
            raise ValueError(f"Invalid tree entry name '{name}': must not be '..' or '.'")
        
        # Construct the full path for the current entry
        path = base_path + name
        
        # Add blobs and recurse for trees
        if type_ == "blob":
            result[path] = oid  # Associate the path with the blob's oid
        elif type_ == "tree":
            result.update(get_tree(oid, f"{path}/"))  # Recursively add tree entries
        else:
            raise ValueError(f"Unknown tree entry type '{type_}'")  # Handle unexpected types
        
    return result  # Return the assembled dictionary of paths and oids


def _empty_current_directory():
    # Traverse the current directory from bottom to top
    for root, dirs, files in os.walk(".", topdown=False):
        # Remove all files that are not ignored
        for file in files:
            path = os.path.join(root, file)
            if not is_ignored(path):
                os.remove(path)
        # Remove directories that are not ignored
        for dir in dirs:
            path = os.path.join(root, dir)
            if not is_ignored(path):
                try:
                    os.rmdir(path)  # Attempt to remove the directory
                except OSError:
                    pass  # Skip if the directory is not empty


def read_tree(tree_oid:str):
    
    _empty_current_directory()  # Clear the current working directory
    
    # Create files based on the tree structure
    for path, oid in get_tree(tree_oid, base_path="./").items():
        os.makedirs(os.path.dirname(path), exist_ok=True) 
        with open(path, "wb") as file:
            file.write(data.get_object(oid))  # Write the object content to the file


def commit(message:str) -> str:
    tree_oid = write_tree()
    commit = f"tree {tree_oid}\n"
    head = data.get_HEAD()
    print(f"Debug: Current HEAD before commit: {head}")
    if head:
        commit += f"parent {head.decode() if isinstance(head, bytes) else head}\n"
    commit += "\n"
    commit += f"{message}\n"
    
    commit_oid = data.hash_object(commit.encode(), "commit")
    data.set_HEAD(commit_oid)
    
    print(f"Commit OID: {commit_oid}")
    
    return commit_oid


Commit = namedtuple('Commit', ['tree','parent','message'])

def get_commit(commit_oid:str) -> Commit:
    parent = None
    
    commit_content:str = data.get_object(commit_oid, "commit").decode()
    lines = iter(commit_content.splitlines())
    for line in itertools.takewhile(operator.truth, lines):
        key, value = line.split(" ", 1)
        if key == "tree":
            tree = value
        elif key == "parent":
            parent = value
        else:
            print(f"Unknown key:{key}")
    
    commit_message:str = "\n".join(lines)
    return Commit(tree=tree, parent=parent, message=commit_message)


def is_ignored(entry_name: str) -> bool:
    # Check if directory should be ignored
    ignored_dirs = ("21git.egg-info", "mygit", ".git", ".21git")
    
    # Split the entry_name using os.path.normpath to ensure correct handling of path separators
    parts = entry_name.split(os.path.sep)
    
    # Check if any part of the path is in ignored_dirs
    return any(part in ignored_dirs for part in parts)
