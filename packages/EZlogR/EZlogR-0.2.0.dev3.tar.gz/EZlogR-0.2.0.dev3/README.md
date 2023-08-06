# EZlogR for Python!
## Overview
[Project info at Pypi](https://pypi.org/project/EZlogR/) <br>
This module helps developers focus on writing code and less time worrying about writing logs. 

## How it works
EZlogR gives a standardized way for developers to write logs, and creates these logs in JSON format. JSON is easily digestable by a multitude of programs and databases. This lets the developer have the option to easily pull the logs into something like MongoDB, a JSON viewing tool, or still be easily human readable due to the simplified and flat nature of the JSON packing.

## Compatibility
This version of EZlogR is compatible with Python3.6 and later.

## Installation
Install EZlogR using pip (if using a Python3 virtualenv or similar) or pip3: <br>
`pip install ezlogr`<br> 
or <br>
`pip3 install ezlogr`

## Usage
Here is a simple python file that shows EZlogR in action.<br>
Filename: `simple_sample.py`
```
#!/usr/bin/env python3
#Step 1: Import ezlogr
import ezlogr

#Step 2: Set some tags
tags = ["Very cool app", "non-prod"]

#Step 3: Set the filename for your logs. (This will automatically append .log to the .py filename like this: 'myfile.py.log')
filename = __file__

#Step 4: Make your logger instance.
logger = ezlogr.Ezlogr(filename=filename, tags=tags)

#Step 5: Now write your code with EZlogR!
import time
logger.info("Here I go writin' logs!")
time.sleep(1)
logger.info("I'm doing it again!")
```

## Output
After using EZlogR, you will see logs like this:<br> 
Filename: `simple_sample.py.log`
```
{'filename': '/Users/jeremy/simple_sample.py', 'log_level': 'info', 'hrtimestamp': 'Wed Jun 17 10:07:23 2020', 'datestamp': '17062020', 'timestamp': '100723.921712', 'log_msg': "Here I go writin' logs!", 'tags': '["Very cool app", "non-prod"]'}
{'filename': '/Users/jeremy/simple_sample.py', 'log_level': 'info', 'hrtimestamp': 'Wed Jun 17 10:07:24 2020', 'datestamp': '17062020', 'timestamp': '100724.926889', 'log_msg': "I'm doing it again!", 'tags': '["Very cool app", "non-prod"]'}
```