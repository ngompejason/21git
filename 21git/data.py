import os 
import hashlib
# import fcntl

GIT_DIR = ".21git"
file_path = os.path.join(GIT_DIR, "HEAD")

def init():
    os.makedirs(GIT_DIR, exist_ok=True)
    os.makedirs(os.path.join(GIT_DIR, "objects"), exist_ok=True)

def set_HEAD(commit_oid:str):
    try:
        # Write the commit_oid to the HEAD file
        with open(file_path, "w") as head:
            head.write(commit_oid)
    except FileNotFoundError:
        print(f"File: {file_path} not found")
    except PermissionError:
        print(f"Permission denied when trying to write to {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_HEAD():
    try:
        with open(file_path, "rb") as file:
            return file.read().strip()
    except Exception as e:
        print(f"Exception: {e}")


def hash_object(file_content:bytes, type_:str="blob") -> str:
    NULL = b'\x00'
    data = type_.encode()+NULL+file_content
    oid:str =hashlib.sha1(data).hexdigest()
    hash_file_path:str = os.path.join(GIT_DIR, "objects", oid)
    with open(hash_file_path, "wb") as out:
        out.write(data)
    
    return oid
    
    
def get_object(oid:str, expected:str = "blob") -> bytes:
    hash_file_path:str = os.path.join(GIT_DIR, "objects", oid)
    with open(hash_file_path, "rb") as f:
        file = f.read()
        
        NULL = b'\x00'
        type_,_,content = file.partition(NULL)
        type_ = type_.decode()
    
    #When expected is provided (not None)
    #the function will check if the object's type matches the expected type.
    #When expected is None, the function will skip the type check entirely.
    if expected is not None and type_ != expected:
        raise ValueError(f'Expected {expected}, got {type_}')
    
    return content