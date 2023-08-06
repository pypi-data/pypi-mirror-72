# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['platonic_queue']

package_data = \
{'': ['*']}

install_requires = \
['boto3[sqs]>=1.14.8,<2.0.0', 'boto3_type_annotations[sqs]>=0.3.1,<0.4.0']

setup_kwargs = {
    'name': 'platonic-queue',
    'version': '0.1.0',
    'description': 'Abstract acknowledgement queue concept, implemented over multiple backends.',
    'long_description': '# platonic-queue\n\n[![Build Status](https://travis-ci.com/platonic/platonic-queue.svg?branch=master)](https://travis-ci.com/platonic/platonic-queue)\n[![Coverage](https://coveralls.io/repos/github/platonic/platonic-queue/badge.svg?branch=master)](https://coveralls.io/github/platonic/platonic-queue?branch=master)\n[![Python Version](https://img.shields.io/pypi/pyversions/platonic-queue.svg)](https://pypi.org/project/platonic-queue/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\nPeople do not program in terms of SQS, tables, and bytes. People program in concepts.  \n\nAbstract acknowledgement queue concept, implemented over multiple backends.\n\n\n## Installation\n\n```bash\npip install platonic-queue\n```\n\n\n## Example\n\nShowcase how your project can be used:\n\n```python\nfrom platonic_queue.sqs import SQSQueue\n\nclass NumbersQueue(SQSQueue[int]):\n    """Sending numbers."""\n    url = \'...\'   # SQS queue URL\n\n    serialize =   str   # type: ignore\n    deserialize = int   # type: ignore\n\nqueue = NumbersQueue()\nqueue.put(5)\nqueue.get()\n# 5\n```\n\n## License\n\n[MIT](https://github.com/platonic/platonic-queue/blob/master/LICENSE)\n\n\n## Credits\n\nThis project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [5dc9d4e0e082ab012a399856368212745f40ed4f](https://github.com/wemake-services/wemake-python-package/tree/5dc9d4e0e082ab012a399856368212745f40ed4f). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/5dc9d4e0e082ab012a399856368212745f40ed4f...master) since then.\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/platonic/platonic-queue',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
