# altf1be_json_helpers

Helpers to deal with basic requirements of the management of a JSON File: Load, save, save with datetime. The library is built by www.alt-f1.be. See <https://bitbucket.org/altf1be/altf1be_json_helpers>

The class [AltF1beJSON](altf1be_json_helpers/altf1be_json_helpers.py) counts a limited amount of methods

* Load a JSON file
* Save a JSON file and create the directory where to store the JSON file if it does not exists
* Save a JSON file appended with a date time; e.g. 2020-06-19_20-45-42 (format YYYY-MM-DD_HH-MM-SS)

## usage

* install the package on **pypi.org** : 
    * install : `pip install altf1be_json_helpers`
    * upgrade : `pip install altf1be_json_helpers --upgrade`


* install the package on **test.pypi.org** : 
    * install : `pip install -i https://test.pypi.org/simple/altf1be_json_helpers`
    * upgrade : `pip install -i https://test.pypi.org/simple/altf1be_json_helpers --upgrade`

## dependencies

* See [requirements.txt](requirements.txt)

## Build the package 

* install NodeJS packages `npm install`

* build the setup.py
    * Clean and build the package : `npm run clean-build`

* upload the library on TEST **pypi.org** 
    * `npm run push-test:setup.py`
    * Source : [https://test.pypi.org/project/altf1be_json_helpers](https://test.pypi.org/project/altf1be_json_helpers)

* upload the library on PROD **pypi.org** 
    * `npm run push-prod:setup.py` 
    * Source : [https://pypi.org/project/altf1be_json_helpers](https://pypi.org/project/altf1be_json_helpers)


## test the library

* `cd altf1be_json_helpers`
* `python altf1be_json_helpers_unittest.py`

* locate the package 
    * `python -c "from altf1be_json_helpers import AltF1BeJSONHelpers as _; print(_.__path__)"` **does not work yet**

* list functions inside the module
    *  the package `python -c "import altf1be_json_helpers as _; print(dir(_))"`

* test the package 
    * `python -c 'import os;from altf1be_json_helpers import AltF1BeJSONHelpers; altF1BeJSONHelpers = AltF1BeJSONHelpers();data = altF1BeJSONHelpers.load(os.path.join("data", "altf1be_sample.json"));print(data)'`
    * result : `{"name": "altf1be_json_helpers"}`

## Documentation

* Packaging Python Projects <https://packaging.python.org/tutorials/packaging-projects/>
* Managing Application Dependencies <https://packaging.python.org/tutorials/managing-dependencies/#managing-dependencies>
* Packaging and distributing projects <https://packaging.python.org/guides/distributing-packages-using-setuptools/#distributing-packages>

## License

Copyright (c) ALT-F1 SPRL, Abdelkrim Boujraf. All rights reserved.

Licensed under the EUPL License, Version 1.2.

See LICENSE in the project root for license information.
