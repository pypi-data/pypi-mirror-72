[![CircleCI](https://circleci.com/gh/ThinkBigAnalytics/AoaPythonClient.svg?style=svg&circle-token=15915df83a6183fa3e0fd86ed21b1d9b91abfd29)](https://circleci.com/gh/ThinkBigAnalytics/AoaPythonClient)

# AnalyticOps Accelerator Python Client

Python client for Teradata AnalyticOps Accelerator. It is composed of both an client API implementation to access the AOA Core APIs and a command line interface (cli) tool which can be used for many common tasks. 


## Requirements

Python 3.6+


## Usage

See the pypi [guide](./docs/pypi.md) for some usage notes. 


## Installation

To install the latest release, just do

```
pip install aoa
```

To build from source, it is advisable to create a Python venv or a Conda environment 

Python venv:
```
python -m venv aoa_python_env
source aoa_python_env/bin/activate
```

Conda environment:
```
conda create -n aoa_python_env -q -y python=3.6
conda activate aoa_python_env
```

Install library from local folder using pip:

```
pip install --upgrade .
```

Install library from package file

```
# first create the package
python setup.py sdist bdist_wheel

# install using pip
pip install dist/*.whl
```

## Testing

```
python setup.py test
```

## Building 

```
python -m pip install --user --upgrade setuptools wheel

python setup.py sdist bdist_wheel

twine upload -u td-aoa -p <user@pass> dist/*

```