
# Setup

## Install required packages

```
sudo apt install python3 python3-pip python3.12-venv
```

## Start and activate a virtual Python environment

```
python3 -m venv path/to/venv
path/to/venv/bin/activate
```

## Install build dependencies (building, test and documentation)

```bash
pip3 install build grpcio-tools==1.62.0           # Build proto files and Python
pip3 install pytest                               # Testing
pip3 install sphinx myst-parser sphinx-rtd-theme  # Documentation
```

# Build

## Package Build
```
python3 -m build
```

## Install the package locally in editable mode
```
pip3 install --editable .
```


## Run the tests
```
python3 -m pytest
```

## Build the documentation
```
sphinx-build -M html ./doc/source/ ./doc/build/
```




