# 21Git: Building Git from Scratch

This project aims to recreate the core functionality of Git from scratch, providing a deep understanding of Git's internal workings.
Right now i just implemented the three low-level commands, will update the repo daily.

## Current Features

- Initialize a new 21Git repository
- Hash and store objects
- Retrieve stored objects

## Usage

### 1. Setting Up the Virtual Environment
First, create and activate your virtual environment:

```bash
python -m venv venv && source venv/bin/activate
```
On Windows: 
```cmd
python -m venv venv
```
```cmd
venv\Scripts\activate
```
### 2. Installing the Package in Editable Mode
Install the package in editable mode from the project directory:
```bash
pip install -e .
```
After the package is installed, you can use the CLI directly.

### Initialize a new repository
```bash
21git init
```
This command creates a new .21git directory with the necessary subdirectories.

### Hash an object
```bash
21git hash-object <file>
```
This command hashes the content of the specified file and stores it in the `.21git/objects` directory.

### Retrieve an object
```bash
21git cat-file <object_hash>
```

This command retrieves and displays the content of the specified object.

## Project Structure

- `cli.py`: Handles command-line interface and argument parsing
- `data.py`: Contains core functionality for object storage and retrieval

## Future Development

This project is still in its early stages. Future updates include:

- Implementing staging area (index)
- Adding commit functionality
- Developing branching and merging capabilities

## License

[MIT License](https://opensource.org/licenses/MIT)
