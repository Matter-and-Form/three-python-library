
# Setup

## Install required packages

```
sudo apt install python3 python3-pip python3.12-venv
```

## Start and activate a virtual Python environment

```
python -m venv path/to/venv
path/to/venv/bin/activate
```

## Install build dependencies (building, test and documentation)

```
pip install --upgrade build pytest sphinx myst-parser sphinx-rtd-theme
```

# Build

## Package Build
```
python3 -m build
```

## Install the package locally in editable mode
```
pip install --editable .
```


## Run the tests
```
python3 -m pytest
```

# Build the documentation
```
sphinx-build -M html ./doc/source/ ./doc/build/
```




