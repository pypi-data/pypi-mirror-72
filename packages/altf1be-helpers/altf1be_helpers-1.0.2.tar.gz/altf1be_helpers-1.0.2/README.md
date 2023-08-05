# altf1be_helpers

Helpers to deal with basic requirements of an application built by www.alt-f1.be. See <https://bitbucket.org/altf1be/altf1be_helpers>

The class ALTF1


* Get the list of countries stored in the field "place" in transactions stored in twikey.
* The places are written either in FR, EN or NL.
* The method returns a List of places in English and a Set of those places if the places are using the above-mentioned languages

## usage

* install the package on **pypi.org** : 
    * install : `pip install altf1be_helpers`
    * upgrade : `pip install altf1be_helpers --upgrade`


* install the package on **test.pypi.org** : 
    * install : `pip install -i https://test.pypi.org/simple/altf1be_helpers`
    * upgrade : `pip install -i https://test.pypi.org/simple/altf1be_helpers --upgrade`

## dependencies

* See [requirements.txt](requirements.txt)

## Build the package 

* build the setup.py
    * `python3 setup.py sdist bdist_wheel`
    * `python3 -m pip install --user --upgrade twine`

* upload the library on TEST **pypi.org** 
    * `python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*` 
    * Source : [https://test.pypi.org/project/altf1be_helpers](https://test.pypi.org/project/altf1be_helpers)

* upload the library on PROD **pypi.org** 
    * `python -m twine upload dist/*` 
    * Source : [https://pypi.org/project/altf1be_helpers](https://pypi.org/project/altf1be_helpers)


## test the library

* `cd altf1be_helpers`
* `python altf1be_helpers_unittest.py`

* locate the package 
    * `python -c "from altf1be_helpers import AltF1BeHelpers as _; print(_.__path__)"` **does not work yet**
* list functions inside the module
    *  the package `python -c "import altf1be_helpers as _; print(dir(_))"`

* test the package 
    * `python -c "from altf1be_helpers import AltF1BeHelpers; text='éê à iïî'; print(f'{AltF1BeHelpers.unicode_to_ascii(text)}')"`
    * result : `ee a iii`

## Documentation

* Packaging Python Projects <https://packaging.python.org/tutorials/packaging-projects/>
* Managing Application Dependencies <https://packaging.python.org/tutorials/managing-dependencies/#managing-dependencies>
* Packaging and distributing projects <https://packaging.python.org/guides/distributing-packages-using-setuptools/#distributing-packages>

## License

Copyright (c) ALT-F1 SPRL, Abdelkrim Boujraf. All rights reserved.

Licensed under the EUPL License, Version 1.2.

See LICENSE in the project root for license information.
