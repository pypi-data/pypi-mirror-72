# OmniPack

A collection of commonly used Python scripts in work.

[![Build Status](https://travis-ci.com/FrankLeeeee/OmniPack.svg?branch=master)](https://travis-ci.com/FrankLeeeee/OmniPack)
[![PyPI version](https://badge.fury.io/py/omnipack.svg)](https://badge.fury.io/py/omnipack)

## Installation

```shell
pip install omnipack
```

## In-Python

OmniPack provides commonly used functions for quick programming. For example, it can load configuration from different kinds of files.

```python
from omnipack import ConfigLoader
import os.path as osp

# load python file as configuration
py_sample_path = osp.join(BASE_DIR, 'data/fileio/sample.py')
py_config = ConfigLoader.from_file(py_sample_path)


# load json
json_sample_path = osp.join(BASE_DIR, 'data/fileio/sample.json')
json_config = ConfigLoader.from_file(json_sample_path)

# load yaml
yaml_sample_path = osp.join(BASE_DIR, 'data/fileio/sample.yaml')
yaml_config = ConfigLoader.from_file(yaml_sample_path)

# load python dictionary
dict_sample = dict(a=1, b=2)
dict_config = ConfigLoader.from_dict(dict_sample)
```

## Command Line Interface

OmniPack provides many easy-to-use commands for convenience purposes. For example, to kill ghost processes triggered by the same command

```shell
omnipack kill_multiprocess "train.py"
```

## Contributor

Li Shenggui
