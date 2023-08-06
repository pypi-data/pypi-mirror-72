# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipynb_path']

package_data = \
{'': ['*']}

install_requires = \
['ipykernel>=4.0,<5.0', 'notebook>=4.0,<5.0', 'requests>=2.0,<3.0']

setup_kwargs = {
    'name': 'ipynb-path',
    'version': '0.1.3',
    'description': 'A simple python package to get the path of the current IPython / Jupyter Notebook file.',
    'long_description': "ipynb-path\n==========\n\nA simple python package to get the path of the current IPython / Jupyter Notebook file.\n\nInstallation\n------------\n\n.. code:: bash\n\n    pip install ipynb-path\n\nUsage\n-----\n\nIf you can access to your Jupyter Notebook/Lab server without a password, \nyou can use just ``ipynb_path.get()`` in a ``.ipynb`` file.\n\n.. code:: python\n\n    import ipynb_path\n    __file__ = ipynb_path.get()\n\nIf you need a password to access the server, you should specify it.\n\n.. code:: python\n\n    import ipynb_path\n    __file__ = ipynb_path.get(password='foo')\n\nYou can also specify ``__name__`` for compatibility between ``.py`` and ``.ipynb``.\nIn this case, ``ipynb_path.get()`` does not overwrite ``__file__`` even if it is called in a ``.py`` file.\n\n.. code:: python\n\n    import ipynb_path\n    __file__ = ipynb_path.get(__name__)\n",
    'author': 'Kazuma Takahara',
    'author_email': '4269kzm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kzm4269/ipynb-path',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
