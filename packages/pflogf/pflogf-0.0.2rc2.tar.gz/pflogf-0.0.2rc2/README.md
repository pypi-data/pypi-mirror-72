# pflogf

[![PyPI version](https://badge.fury.io/py/pflogf.svg)](https://pypi.org/project/pflogf/)

Colorful logging formatter for fnndsc/pf* family.
Its hardcoded format displays displays time, hostname, and calling function.
The various logging levels (debug, info, warn, error, critical) are printed in different colors.

pflogf aims to replace [pfmisc/debug.py](https://github.com/FNNDSC/pfmisc/blob/master/pfmisc/debug.py)
using the standard Python [logging](https://docs.python.org/3/library/logging.html) module.

## Screenshots

The output is intended for full-screen TTY output.

![full screen](docs/wide.png)

It tries to detect when not enough colums are available to display full information.

![half screen](docs/narrow.png)

## Examples

```python
import logging
from pflogf import FnndscLogFormatter

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(FnndscLogFormatter())
logger.addHandler(handler)

logger.setLevel(logging.DEBUG)
logger.debug('debug me as I am full of bugs')
logger.info('an informative statement')
logger.warning('you\'ll probably ignore this warning')
logger.error('error, problem exists between keyboard and chair')
logger.critical('critical failure, haha jk')
```
