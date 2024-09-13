import argparse
import os
from . import data

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
    
    #add ''hash-object' subcmmmand
    hash_object_parser = commands.add_parser("hash-object")
    hash_object_parser.set_defaults(func=hash_object)
    hash_object_parser.add_argument("file")
    
    return parser.parse_args()

def init(args):
    # Placeholder function for 'init' command
    # print("I'm the init function")
    data.init()
    print(f"Initialized an empty 21git repository in the {os.path.join(os.getcwd(), data.GIT_DIR)}")

def hash_object(args):
    with open(args.file, "rb") as f:
        print(data.hash_object(f.read()))