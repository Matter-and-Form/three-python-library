
# Setup

## Install required packages

```
sudo apt install python3 python3-pip python3.12-venv
```

## Start and activate a virtual Python environment with the build dependencies

```
python3 -m venv .venv
source .venv/bin/activate && pip3 install -r requirements.txt
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




