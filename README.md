# chaostoolkit-chaoshub

[![Build Status](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-chaoshub.svg?branch=master)](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-chaoshub)

The Chaos Hub plugin library.

## Purpose

The purpose of this library is to provide [Chaos Hub][] collaboration and sharing
 support to the [Chaos Toolkit][chaostoolkit].

[chaostoolkit]: http://chaostoolkit.org
[chaoshub]: http://chaoshub.com

## Features

The library adds the ability to login to a Chaos Hub, by default [ChaosHub.com][chaoshub], 
and then to be able to publish experiment's and experimental findings into the hub.

## Install

Install this package as any other Python packages:

```
$ pip install -U chaostoolkit-chaoshub
```

Notice that this draws a few [dependencies][deps]:

[deps]: https://github.com/chaostoolkit-incubator/chaostoolkit-chaoshub/blob/master/requirements.txt


## Usage

Once installed, new `login` and `publish` subcommands will be made available to the
`chaos` command. You can use them as follows:

```
$ chaos login
```

```
$ chaos publish journal.json
```

The `login` command sets up your chaos toolkit installation to target a particular 
Chaos Hub. The `chaos publish` command enables you to manually push your experimental 
findings, typically recorded in the `journal.json`, to your Chaos Hub account.

By default, once you have logged into your Chaos Hub you will automatically publish
your experiment's findings to your own organization and workspace when you execute 
`chaos run`. You can turn this behaviour off by specifying `--no-publish` as shown here:

```
$ chaos run experiment.json --no-publish
```

## Contribute

Contributors to this project are welcome as this is an open-source effort that
seeks [discussions][join] and continuous improvement.

[join]: https://join.chaostoolkit.org/

From a code perspective, if you wish to contribute, you will need to run a 
Python 3.5+ environment. Then, fork this repository and submit a PR. The
project cares for code readability and checks the code style to match best
practices defined in [PEP8][pep8]. Please also make sure you provide tests
whenever you submit a PR so we keep the code reliable.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

### Develop

If you wish to develop on this project, make sure to install the development
dependencies. But first, [create a virtual environment][venv] and then install
those dependencies.

[venv]: http://chaostoolkit.org/reference/usage/install/#create-a-virtual-environment

```console
$ pip install -r requirements-dev.txt -r requirements.txt 
```

Then, point your environment to this directory:

```console
$ python setup.py develop
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the tests for the project execute the following:

```
$ pytest
```
