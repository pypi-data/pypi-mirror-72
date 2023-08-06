# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ekrhizoc', 'ekrhizoc.bot.crawlers', 'ekrhizoc.cli.commands']

package_data = \
{'': ['*'], 'ekrhizoc': ['bot/*', 'bot/helpers/*', 'cli/*']}

install_requires = \
['aiodns>=2.0,<3.0',
 'aiohttp>=3.6,<4.0',
 'asyncio>=3.4,<4.0',
 'beautifulsoup4>=4.8,<5.0',
 'matplotlib>=3.1,<4.0',
 'networkx>=2.4,<3.0',
 'pyyaml>=5.3,<6.0',
 'reppy>=0.4,<0.5',
 'urlcanon>=0.3,<0.4']

entry_points = \
{'console_scripts': ['ekrhizoc = ekrhizoc.cli.__main__:main']}

setup_kwargs = {
    'name': 'ekrhizoc',
    'version': '0.1.2',
    'description': 'A simple python web crawler',
    'long_description': '[![github latest release](https://badgen.net/github/release/nichelia/ekrhizoc?icon=github)](https://github.com/nichelia/ekrhizoc/releases/latest/)\n[![pypi latest package](https://badgen.net/pypi/v/ekrhizoc?label=pypi%20pacakge)](https://pypi.org/project/ekrhizoc/)\n[![docker latest image](https://img.shields.io/docker/v/nichelia/ekrhizoc?label=image&logo=docker&logoColor=white)](https://hub.docker.com/repository/docker/nichelia/ekrhizoc)\n[![project license](https://badgen.net/github/license/nichelia/ekrhizoc?color=purple)](https://github.com/nichelia/ekrhizoc/blob/master/LICENSE)\n\n![e6c CI](https://github.com/nichelia/ekrhizoc/workflows/e6c%20CI/badge.svg)\n![e6c CD](https://github.com/nichelia/ekrhizoc/workflows/e6c%20CD/badge.svg)\n[![security scan](https://badgen.net/dependabot/nichelia/ekrhizoc/?label=security%20scan)](https://github.com/nichelia/ekrhizoc/labels/security%20patch)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen)](https://github.com/pre-commit/pre-commit)\n\n\n[![code coverage](https://badgen.net/codecov/c/github/nichelia/ekrhizoc?label=code%20coverage)](https://codecov.io/gh/nichelia/ekrhizoc)\n[![code alerts](https://badgen.net/lgtm/alerts/g/nichelia/ekrhizoc?label=code%20alerts)](https://lgtm.com/projects/g/nichelia/ekrhizoc/alerts/)\n[![code quality](https://badgen.net/lgtm/grade/g/nichelia/ekrhizoc?label=code%20quality)](https://lgtm.com/projects/g/nichelia/ekrhizoc/context:python)\n[![code style](https://badgen.net/badge/code%20style/black/color=black)](https://github.com/ambv/black)\n\n# ekrhizoc\nekrhizoc (E6c): A web crawler\n\n## Contents\n1. [Definition](#definition)\n2. [Use Case](#use-case)\n3. [Configuration](#configuration)\n4. [Development](#development)\n5. [Testing](#testing)\n6. [Versioning](#versioning)\n7. [Deployment](#deployment)\n8. [Production](#production)\n\n## Definition\n\nεκρίζωση (Greek)\nekrízosi / uprooting, eradication\n\nAlso known as __E6c__.\n\n## Use Case\n\nImplementation of a simple python web crawler.  \nInput: URL (seed).  \nOutput: Simple textual sitemap (to show links between pages).\n\n### Requirements\n\n* The crawler is limited to *__one__* subdomain (exclude external links).\n* No use of web crawling libraries/frameworks (e.g. scrapy).\n* (Optional) Use of HTML handling Libraries/Frameworks.\n* Production-ready code.\n\n### Assumptions\n\n* The input URL (seed) is limited to __only__ one at every run.\n* The targeted URL(s) are static pages (no backend javascript parsing required).\n* Links to be extracted from HTML anchor `<a>` elements.\n* Valid links include\n    - Valid URL\n        + Non empty\n        + Matches a valid url pattern\n        + Does not exceed the `E6C_MAX_URL_LENGTH` length in characters\n        + Possible to convert a relative urls to a full url\n    - Link is not visited before\n    - Link is not part of an ignored file type\n    - Link has the same domain as the seed url\n    - Link is not restricted by the robots.txt file\n\n### Design\n\nThis project implements a Basic Universal Crawler based on breadth first search graph traversal.\n\n## Configuration\n\nBehaviour of the application can be configured via Environment Variables.\n\n| Environment Variable | Description | Type | Default Value |\n| -------------- | -------------- | -------------- | -------------- |\n| `E6C_LOG_LEVEL` | Level of logging - overrides verbose/quiet flag | string | - |\n| `E6C_LOG_DIR` | Directory to save logs | string | - |\n| `E6C_BIN_DIR` | Directory to save any output (bin) | string | bin |\n| `E6C_IGNORE_FILETYPES` | File types of websites to ignore (e.g. ".filetype1,.filetype2") | string | ".png,.pdf,.txt,.doc,.jpg,.gif" |\n| `E6C_URL_REQUEST_TIMER` | Time (in seconds) to wait per request (not to populate server with multiple requests) | float | 0.1 |\n| `E6C_MAX_URLS` | The maximum number of urls to fetch/crawl | integer | 10000 |\n| `E6C_MAX_URL_LENGTH` | The maximum length (character count) of a url to fetch/crawl | integer | 300 |\n\n## Development\n\n### Configure your local development\n\n* Clone [repo](https://github.com/nichelia/ekrhizoc) on your local machine\n* Install [`conda`](https://www.anaconda.com) or [`miniconda`](https://docs.conda.io/en/latest/miniconda.html)\n* Create your local project environment (based on [`conda`](https://www.anaconda.com), [`poetry`](https://python-poetry.org), [`pre-commit`](https://pre-commit.com)):  \n`$ make env`\n* (Optional) Update existing local project environment:  \n`$ make env-update`\n\n### Run locally\n\nOn a terminal, run the following (execute on project\'s root directory):\n\n* Activate project environment:  \n`$ . ./scripts/helpers/environment.sh`\n* Run the CLI using `poetry`:  \n`$ ekrhizoc`\n\n### Contribute\n\n[ Not Available ]\n\n## Testing\n(part of CI/CD)\n\n[ Work in progress... ]\n\nTo run the tests, open a terminal and run the following (execute on project\'s root directory):\n\n* Activate project environment:  \n`$ . ./scripts/helpers/environment.sh`\n* To run pytest:  \n`$ make test`\n* To check test coverage:  \n`$ make test-coverage`\n\n## Versioning\n\nIncrement the version number:  \n`$ poetry version {bump rule}`  \nwhere valid bump rules are:\n\n1. patch\n2. minor\n3. major\n4. prepatch\n5. preminor\n6. premajor\n7. prerelease\n\n### Changelog\n\nUse `CHANGELOG.md` to track the evolution of this package.  \nThe `[UNRELEASED]` tag at the top of the file should always be there to log the work until a release occurs.  \n\nWork should be logged under one of the following subtitles:\n* Added\n* Changed\n* Fixed\n* Removed\n\nOn a release, a version of the following format should be added to all the current unreleased changes in the file.  \n`## [major.minor.patch] - YYYY-MM-DD`\n\n## Deployment\n\n### Pip package\n\nOn a terminal, run the following (execute on project\'s root directory):\n\n* Activate project environment:  \n`$ . ./scripts/helpers/environment.sh`\n* To build pip package:  \n`$ make build-package`\n* To publish pip package (requires credentials to PyPi):  \n`$ make publish-package`\n\n### Docker image\n\nOn a terminal, run the following (execute on project\'s root directory):\n\n* Activate project environment:  \n`$ . ./scripts/helpers/environment.sh`\n* To build docker image:  \n`$ make build-docker`\n\n## Production\n\nFor production, a Docker image is used.\nThis image is published publicly on [docker hub](https://hub.docker.com/repository/docker/nichelia/ekrhizoc).\n\n* First pull image from docker hub:  \n`$ docker pull nichelia/ekrhizoc:{version}`\n* Execute CLI via docker run:  \n`$ docker run --rm -it -v ~/ekrhizoc_bin:/tmp/bin nichelia/ekrhizoc:{version} {command}`  \nThis command mounts the application\'s bin (outcome) to user\'s root directory under ekrhizoc_bin folder.\n\nwhere version is the published application version\n',
    'author': 'Nicholas Elia',
    'author_email': 'me@nichelia.com',
    'maintainer': 'Nicholas Elia',
    'maintainer_email': 'me@nichelia.com',
    'url': 'https://github.com/nichelia/ekrhizoc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
