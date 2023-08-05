# PyLib
Python pckg

Usage:

```sh

$ sudo apt-get install python3 python3-pip
$ sudo pip3 install -r requirements.txt
$ sudo pip3 install -e .                   
$ sudo python3 setup.py sdist bdist_wheel
$ sudo twine upload --skip-existing dist/*

```

```cmd

C:\> pip3 install -r requirements.txt
C:\> pip install -e .                   
C:\> python setup.py sdist                              
C:\> twine upload --skip-existing dist/*

```

> cmd commands history

```sh
┌────────────────────────────────────────┐
│0: pip install -e .                     │
│1: python setup.py sdist                │
│2: pip install -e .                     │
│3: twine upload --skip-existing dist/*  │
└────────────────────────────────────────┘


```

Description: This project provides powerful math functions
        |For example, you can use `sum()` to sum numbers:
        |
        |Example::
        |
        |    >>> sum(1, 2)
        |    3
        |