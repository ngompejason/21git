import os 
import hashlib

GIT_DIR = ".21git"

def init():
    os.makedirs(GIT_DIR, exist_ok=True)
    os.makedirs(os.path.join(GIT_DIR, "objects"), exist_ok=True)
    

def hash_object(data:bytes) -> str:
    oid:str =hashlib.sha1(data).hexdigest()
    hash_file_path:str = os.path.join(GIT_DIR, "objects", oid)
    with open(hash_file_path, "wb") as out:
        out.write(data)
    
    return oid
    
    
def get_object(oid:str) -> bytes:
    hash_file_path:str = os.path.join(GIT_DIR, "objects", oid)
    with open(hash_file_path, "rb") as file:
        return file.read()