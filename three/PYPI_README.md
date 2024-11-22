# Matter and Form THREE Library

## Overview
The Matter and Form THREE library provides a comprehensive API for controlling and interacting with the Matter and Form THREE scanner. This library allows developers to build custom integrations, automate tasks, and create new front-end systems for 3D scanning.

## Project Home
[Github Project HERE](https://github.com/Matter-and-Form/three-python-library).

## Examples 

### Using Premade Examples
To connect to the scanner, you can use the provided examples. For instance, to run the connection example, execute:

```sh
python examples/connect.py
```

### Simple Example
Here is an example of how to use the library to connect to the scanner and control the projector:

```python
from matter_and_form_three import Scanner

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

### More Examples
The library comes with several pre-made examples. You can find them in the [examples directory](https://github.com/Matter-and-Form/three-python-library/tree/develop/three/examples).

To run a specific example, use:

```sh
python three/examples/<example_name>.py
```

## Documentation
For detailed documentation, visit the TODO -> [official documentation](https://github.com/Matter-and-Form/three-python-library/wiki).


## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.