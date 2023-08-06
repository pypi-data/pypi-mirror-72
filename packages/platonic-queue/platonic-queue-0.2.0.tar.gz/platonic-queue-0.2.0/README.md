# platonic-queue

[![Build Status](https://travis-ci.com/platonic/platonic-queue.svg?branch=master)](https://travis-ci.com/platonic/platonic-queue)
[![Coverage](https://coveralls.io/repos/github/platonic/platonic-queue/badge.svg?branch=master)](https://coveralls.io/github/platonic/platonic-queue?branch=master)
[![Python Version](https://img.shields.io/pypi/pyversions/platonic-queue.svg)](https://pypi.org/project/platonic-queue/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

People do not program in terms of SQS, tables, and bytes. People program in concepts.  

Abstract acknowledgement queue concept, implemented over multiple backends.


## Installation

```bash
pip install platonic-queue
```


## Example

Showcase how your project can be used:

```python
from platonic_queue.sqs import SQSBaseQueue

class NumbersQueue(SQSBaseQueue[int]):
    """Sending numbers."""
    url = '...'   # SQS queue URL

    serialize =   str   # type: ignore
    deserialize = int   # type: ignore

queue = NumbersQueue()
queue.put(5)
queue.get()
# 5
```

## License

[MIT](https://github.com/platonic/platonic-queue/blob/master/LICENSE)


## Credits

This project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [5dc9d4e0e082ab012a399856368212745f40ed4f](https://github.com/wemake-services/wemake-python-package/tree/5dc9d4e0e082ab012a399856368212745f40ed4f). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/5dc9d4e0e082ab012a399856368212745f40ed4f...master) since then.
