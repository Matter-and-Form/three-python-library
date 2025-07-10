# Matter and Form THREE Library

## Overview
The Matter and Form THREE library provides a comprehensive API for controlling and interacting with the Matter and Form THREE scanner. This library allows developers to build custom integrations, automate tasks, and create new front-end systems for 3D scanning.

## Setup

### Install Required Packages
Ensure you have Python 3.10 or newer installed. You can download it from [python.org](https://www.python.org).

### Initialize Git Submodules
If you haven't already initialized the git submodules, run the following command:

```sh
git submodule update --init --recursive
```

### Start and Activate a Virtual Python Environment
Create and activate a virtual environment:

```sh
python -m venv .venv
source .venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Requirements
Install the required packages listed in the `requirements.txt` file:

```sh
pip install -r requirements.txt
```

### Build

#### Build Python Source from Proto Files
This is only necessary if you have an update the schema. Keep in mind that schema's are tied to THREE server releases. Generated files are commited to this repo.To generate the Python source files again from the Schema files, run:

```sh
python3 ./scripts/build_proto.py
```

#### Package Build
To build the package, run:

```sh
python -m build```

#### Install the Package Locally in Editable Mode
To install the package locally in editable mode, run:

```sh
pip install -e .
```

#### Run the Tests
At the moment there are no unit tests

#### Build the Documentation
To build the documentation, run:

```sh
python ./scripts/build_doc.py
```

## How to Use the Library

### Installation from PyPI
To install the library from PyPI, run:

```sh
pip install mfthree
```

### Connect to the Scanner
To connect to the scanner, you can use the provided examples. For instance, to run the connection example, execute:

```sh
python examples/connect.py
```

### Example Usage
Here is an example of how to use the library to connect to the scanner and control the projector:

```python
from three.scanner import Scanner

# Create and connect to the scanner
scanner = Scanner(OnTask=None, OnMessage=None, OnBuffer=None)
# Use the Zeroconf address or replace with the ip
scanner.Connect("ws://matterandform.local:8081")

# Simple request to list all projects
projectTask = scanner.list_projects()

# Check the output from the task for errors
if projectTask.Error:
    print('Error:', projectTask.Error)
    return
# Do something with the output
for project_obj in projectTask.Output:
    project = Project.Brief(**project_obj)
    print('Project index:', project.index, ' - Name:', project.name)
```

### Available Examples
The library comes with several pre-made examples. You can find them in the [examples directory](https://github.com/Matter-and-Form/three-python-library/tree/develop/three/examples).

To run a specific example, use:

```sh
python three/examples/<example_name>.py
```

## Documentation
For detailed documentation, visit the [official documentation](https://matter-and-form.github.io/three-python-library/three/scanner.html).

## Contributing
We welcome contributions! Please follow the standard GitHub workflow:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
