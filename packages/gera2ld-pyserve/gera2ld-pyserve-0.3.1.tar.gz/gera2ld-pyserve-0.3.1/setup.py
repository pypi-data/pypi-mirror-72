# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gera2ld', 'gera2ld.pyserve']

package_data = \
{'': ['*']}

extras_require = \
{'aio': ['aiohttp>=3.6.2,<4.0.0']}

setup_kwargs = {
    'name': 'gera2ld-pyserve',
    'version': '0.3.1',
    'description': 'Start serving an asyncio.Server',
    'long_description': "gera2ld.pyserve\n===============\n\n.. image:: https://img.shields.io/pypi/v/gera2ld-pyserve.svg\n\nServe asyncio and aiohttp servers, and show information for development.\n\nInstallation\n------------\n\n.. code-block:: sh\n\n    $ pip install gera2ld-pyserve\n\n    # or with extra `aio` if aiohttp applications are to be served\n    $ pip install gera2ld-pyserve[aio]\n\nUsage\n-----\n\nRun an asynchronous function in an infinite event loop:\n\n.. code-block:: python\n\n    from gera2ld.pyserve import run_forever\n\n    async def main():\n        # do stuff\n\n    run_forever(main())\n\nStart a server:\n\n.. code-block:: python\n\n    from gera2ld.pyserve import run_forever, start_server_asyncio\n\n    def handle(reader, writer):\n        # add more code here...\n\n    run_forever(start_server_asyncio(handle, ':4000'))\n\nStart a server with `aiohttp`:\n\n.. code-block:: python\n\n    from gera2ld.pyserve import run_forever, start_server_aiohttp\n    from aiohttp import web\n\n    app = web.Application()\n    # add more code here...\n\n    run_forever(start_server_aiohttp(app, ':4000'))\n",
    'author': 'Gerald',
    'author_email': 'gera2ld@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gera2ld/pyserve',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
