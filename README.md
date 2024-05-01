
# Setup
```
sudo apt install python3 python3-pip python3.12-venv

```

python3 -m venv path/to/venv


pip3 install --extra-index-url https://test.pypi.org/simple/ --no-cache-dir --upgrade maf-three



pip3 install sphinx
pip3 install myst-parser
pip install sphinx-rtd-theme


sphinx-build -M html ./source/ ../docs




## Install required packages
```
scripts/install-dependencies
```

# Build the package
```
./scripts/build-package 1.2.3
```


# Start the Virtual Environment
```
scripts/start-virtual-env
```


# Examples

## Install Python OpenCV 
```
sudo apt install python3-opencv
```

## Run the example
```
python3 examples/simpleScanner.py 
```
