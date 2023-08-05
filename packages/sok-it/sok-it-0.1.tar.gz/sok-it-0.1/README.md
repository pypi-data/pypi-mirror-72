<p align="center"><img src="https://api.nikz.in/icon/256-FFF-S-F72D2D-00B7FF" alt="SOC-IT" width="250"/></p>

# sok-it

> Socket /ˈsɒkɪt/

[![pypi](https://img.shields.io/badge/pypi-0.1-informational)](https://pypi.org/project/sok-it/) &nbsp;
[![python](https://img.shields.io/badge/python-v3.6-informational)](https://www.python.org/downloads/) &nbsp;
[![license](https://img.shields.io/badge/license-MIT-green)](https://github.com/nikhiljohn10/sok-it/blob/master/LICENSE)

A python pip package that provide a program to create python sockets

## Installation

The latest released version of the package can be installed using `pip` (or `pip3` if using Python 3):

`pip install sok-it`

Alternatively you can install the latest development version using:

`pip install git+{https,ssh}://git@github.com/nikhiljohn10/sok-it`

## Usage

The **sok-it** package provides `createsocket` command in the shell. It only take one argument, which is the file path of socket to be created.

`createsocket filename`

#### Example

```
createsocket example.sock
createsocket ~/.local/example.sock
```
