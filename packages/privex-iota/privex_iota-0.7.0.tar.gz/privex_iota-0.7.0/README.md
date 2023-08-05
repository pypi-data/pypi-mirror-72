Privex's Random IOTA Tools
==========================

[![Build Status](https://travis-ci.com/Privex/iota-tools.svg?branch=master)](https://travis-ci.com/Privex/iota-tools) 
[![Codecov](https://img.shields.io/codecov/c/github/Privex/iota-tools)](https://codecov.io/gh/Privex/iota-tools)  
[![PyPi Version](https://img.shields.io/pypi/v/privex-iota.svg)](https://pypi.org/project/privex-iota/)
![License Button](https://img.shields.io/pypi/l/privex-iota) 
![PyPI - Downloads](https://img.shields.io/pypi/dm/privex-iota)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/privex-iota) 
![GitHub last commit](https://img.shields.io/github/last-commit/Privex/iota-tools)

IOTA library and command line tools for interacting with IOTA Hornet server API

WARNING: Still under construction

```
+===================================================+
|                 © 2020 Privex Inc.                |
|               https://www.privex.io               |
+===================================================+
|                                                   |
|        Privex's Random IOTA Tools                 |
|        License: X11/MIT                           |
|                                                   |
|        Core Developer(s):                         |
|                                                   |
|          (+)  Chris (@someguy123) [Privex]        |
|                                                   |
+===================================================+

Privex's Random IOTA Tools
Copyright (c) 2020    Privex Inc. ( https://www.privex.io )

```

Install
=======


```sh
# Install/Upgrade privex-iota using pip3 as root
sudo -H python3.8 -m pip install -U privex-iota
```

Usage

```
# Show status information for local IOTA node at http://localhost:14265
iota-status

# Show status information for a remote IOTA node
iota-status https://iota.se1.privex.cc

# Show status information as raw JSON instead of colourful human output
iota-status --raw
iota-status --raw https://iota.se1.privex.cc

# Show help
iota-status --help
iota-status -h

####
# Alternatively invoke as a python module (works the same as iota-status executable)
####

# Show status information for local IOTA node at http://localhost:14265
python3.8 -m privex.iota
# Show status information for a remote IOTA node
python3.8 -m privex.iota https://iota.se1.privex.cc

```


