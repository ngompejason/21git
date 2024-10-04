import argparse
import os
import sys
from . import data
from . import base
import textwrap


def main():
    # parse command line arguments and execute the appropriate function
    args = git_parse_args()
    args.func(args)

def git_parse_args():
    
    # Create the main parser
    parser = argparse.ArgumentParser(description="the parser of my git")
    
    # Add subparsers for different commands
    commands = parser.add_subparsers(dest="command")
    commands.required = True
    
    # Add 'init' subcommand
    init_parser = commands.add_parser("init")
    init_parser.set_defaults(func=init)
    
    #add 'hash-object' subcommmand
    hash_object_parser = commands.add_parser("hash-object")
    hash_object_parser.set_defaults(func=hash_object)
    hash_object_parser.add_argument("file")
    
    #add 'cat-file' subcommmand
    cat_file_parser = commands.add_parser("cat-file")
    cat_file_parser.set_defaults(func=cat_file)
    cat_file_parser.add_argument("object")
    
    #add 'write-tree' subcommmand
    write_tree_parser = commands.add_parser('write-tree')
    write_tree_parser.set_defaults(func=write_tree)
    
    #add 'read-tree' subcommand
    read_tree_parser = commands.add_parser('read-tree')
    read_tree_parser.set_defaults(func=read_tree)
    read_tree_parser.add_argument('tree')
    
    #add 'commit' subcommand
    commit_parser = commands.add_parser('commit')
    commit_parser.set_defaults(func=commit)
    commit_parser.add_argument('-m', '--message', required=True)
    
    #add 'log' subcommand
    log_parser = commands.add_parser('log')
    log_parser.set_defaults(func=log_func)
    log_parser.add_argument("oid", nargs="?")
    
    return parser.parse_args()

def init(args):
    # Placeholder function for 'init' command
    # print("I'm the init function")
    data.init()
    print(f"Initialized an empty 21git repository in the {os.path.join(os.getcwd(), data.GIT_DIR)}")

def hash_object(args):
    with open(args.file, "rb") as f:
        print(data.hash_object(f.read()))
        
def cat_file(args):
    sys.stdout.flush()
    sys.stdout.buffer.write(data.get_object(args.object,expected=None))
    
def write_tree(args):
    print(base.write_tree())
    
    
def read_tree(args):
    base.read_tree(args.tree)


def commit(args):
    base.commit(args.message)


def log_func(args):
    oid_HEAD:str = args.oid or data.get_HEAD()
    while oid_HEAD:
        commit_info = base.get_commit(oid_HEAD)
        print(f"commit: {oid_HEAD}\n")
        print(textwrap.indent(commit_info.message,"    "))
        print("-"*40)
        
        oid_HEAD = commit_info.parent