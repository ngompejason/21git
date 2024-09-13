import os 
import hashlib

GIT_DIR = ".21git"

def init():
    os.makedirs(GIT_DIR, exist_ok=True)
    os.makedirs(os.path.join(GIT_DIR, "objects"), exist_ok=True)
    

def hash_object(data:bytes):
    oid:str =hashlib.sha1(data).hexdigest()
    hash_file_path:str = os.path.join(GIT_DIR, "objects", oid)
    with open(hash_file_path, "wb") as out:
        out.write(data)
    
    return oid
        