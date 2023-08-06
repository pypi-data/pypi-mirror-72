# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['noerr']
setup_kwargs = {
    'name': 'noerr',
    'version': '1.0.0a0',
    'description': 'Catch exceptions via a context manager in Python',
    'long_description': '# noerr\n\nCatch exceptions via context manager in Python.\n\nSuper simple to use:\n\n```python\nfrom noerr import no_err\n\nwith no_err:\n    raise Exception("This won\'t crash my code!")\n\nprint("Yup, still going with no error!")\n```\n\nAlso possible to log errors:\n\n\n```python\nfrom noerr import log_err\n\nwith log_err:\n    raise Exception("Should probably warn the user about this one.")\n\nprint("We now see the error, but don\'t stop because of it")\n```\n\nOutputs:\n```\nException logged by "LogError"\nTraceback (most recent call last):\n  File "<input>", line 4, in <module>\nException: Should probably warn the user about this one.\n\nWe now see the error, but don\'t stop because of it\n```\n\n## Install \n\n```\npip install noerr\n```\n\n## License \n\nMIT License - Copyright (c) 2020 Chris Griffith - See LICENSE\n',
    'author': 'Chris Griffith',
    'author_email': 'chris@cdgriffith.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
