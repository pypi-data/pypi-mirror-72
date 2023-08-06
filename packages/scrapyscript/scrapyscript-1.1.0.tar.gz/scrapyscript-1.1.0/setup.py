# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['scrapyscript']

package_data = \
{'': ['*']}

install_requires = \
['billiard==3.6.3.0', 'scrapy>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'scrapyscript',
    'version': '1.1.0',
    'description': 'Run a Scrapy spider programmatically from a script or a Celery task - no project required.',
    'long_description': '![Build](https://github.com/jschnurr/scrapyscript/workflows/Tests/badge.svg) [![PyPI](https://img.shields.io/pypi/v/scrapyscript.svg)](https://pypi.org/project/scrapyscript/)\n\n# Overview\n\nScrapyscript provides a minimalist interface for invoking Scrapy directly\nfrom your code. Define Jobs that include your spider and any object\nyou would like to pass to the running spider, and then pass them to an\ninstance of Processor which will block, run the spiders, and return a list\nof consolidated results.\n\nUseful for leveraging the vast power of Scrapy from existing code, or to\nrun Scrapy from a Celery job.\n\n# Requirements\n\n- Python 3.6+\n- Tested on Linux only (other platforms may work as well)\n\n# Install\n\n```python\npip install scrapyscript\n```\n\n# Example\n\nLet\'s create a spider that retrieves the title attribute from two popular websites.\n\n``` python\nfrom scrapyscript import Job, Processor\nfrom scrapy.spiders import Spider\nfrom scrapy import Request\nimport json\n\n# Define a Scrapy Spider, which can accept *args or **kwargs\n# https://doc.scrapy.org/en/latest/topics/spiders.html#spider-arguments\nclass PythonSpider(Spider):\n    name = \'myspider\'\n\n    def start_requests(self):\n        yield Request(self.url)\n\n    def parse(self, response):\n        title = response.xpath(\'//title/text()\').extract()\n        return {\'url\': response.request.url, \'title\': title}\n\n# Create jobs for each instance. *args and **kwargs supplied here will\n# be passed to the spider constructor at runtime\ngithubJob = Job(PythonSpider, url=\'http://www.github.com\')\npythonJob = Job(PythonSpider, url=\'http://www.python.org\')\n\n# Create a Processor, optionally passing in a Scrapy Settings object.\nprocessor = Processor(settings=None)\n\n# Start the reactor, and block until all spiders complete.\ndata = processor.run([githubJob, pythonJob])\n\n# Print the consolidated results\nprint(json.dumps(data, indent=4))\n```\n\n``` json\n[\n    {\n        "title": [\n            "Welcome to Python.org"\n        ],\n        "url": "https://www.python.org/"\n    },\n    {\n        "title": [\n            "The world\'s leading software development platform \\u00b7 GitHub",\n            "1clr-code-hosting"\n        ],\n        "url": "https://github.com/"\n    }\n]\n```\n\n# Spider Output Types\nAs per the [scrapy docs](https://doc.scrapy.org/en/latest/topics/spiders.html), a Spider\nmust return an iterable of **Request** and/or **dicts** or **Item** objects.\n\nRequests will be consumed by Scrapy inside the Job. Dicts or Item objects will be queued\nand output together when all spiders are finished.\n\nDue to the way billiard handles communication between processes, each dict or item must be\npickle-able using pickle protocol 0.\n\n# Jobs\n A job is a single request to call a specific spider, optionally passing in\n *args or **kwargs, which will be passed through to the spider constructor at runtime.\n\n```python\ndef __init__(self, spider, *args, **kwargs):\n    \'\'\'Parameters:\n        spider (spidercls): the spider to be run for this job.\n    \'\'\'\n```\n\n# Processor\nA Twisted reactor for running spiders. Blocks until all have finished.\n\n## Constructor\n\n```python\nclass Processor(Process):\n    def __init__(self, settings=None):\n        \'\'\'\n        Parameters:\n          settings (scrapy.settings.Settings) - settings to apply. Defaults to Scrapy defaults.\n        \'\'\'\n```\n\n## Run\n\nStarts the Scrapy engine, and executes all jobs.  Returns consolidated results in a single list.\n\n```python\n    def run(self, jobs):\n        \'\'\'\n        Parameters:\n            jobs ([Job]) - one or more Job objects to be processed.\n\n        Returns:\n            List of objects yielded by the spiders after all jobs have run.\n        \'\'\'\n```\n\n# Notes\n\n## Multiprocessing vs Billiard\n\nScrapyscript spawns a subprocess to support the Twisted reactor. Billiard\nprovides a fork of the multiprocessing library that supports Celery. This\nallows you to schedule scrapy spiders to run as Celery tasks.\n\n# Contributing\n\nUpdates, additional features or bug fixes are always welcome.\n\n## Setup\n- Install (Poetry)[https://python-poetry.org/docs/#installation]\n- `poetry install`\n\n## Tests\n- `make test` or `make tox`\n\n# Version History\n\n- 1.1.0 - 27-Jun-2020 - Python 3.6+ only, dependency version bumps\n- 1.0.0 - 10-Dec-2017 - API changes to pass *args and **kwargs to running spider\n- 0.1.0 - 28-May-2017 - patches to support Celery 4+ and Billiard 3.5.+. Thanks to @mrge and @bmartel.\n\n# License\n\nThe MIT License (MIT). See LICENCE file for details.\n',
    'author': 'Jeff Schnurr',
    'author_email': 'jschnurr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jschnurr/scrapyscript',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
