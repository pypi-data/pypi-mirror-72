#!/usr/bin/env python3

#Step 1: Import ezlogr
from .. import ezlogr

#Step 2: Set some tags
tags = ["Very cool app", "non-prod"]

#Step 3: Set the filename for your logs. (This will automatically append .log to the .py filename like this: 'myfile.py.log')
filename = __file__

#Step 4: Make your logger instance.
logger = ezlogr.Ezlogr(filename=filename, tags=tags)

#Step 5: Now write your code with EZlogR!
logger.debug("Here is a debug log.")
logger.info("Here is an info log.")
logger.warn("Here is a warning log.")
logger.critical("Here is a critical log.")

