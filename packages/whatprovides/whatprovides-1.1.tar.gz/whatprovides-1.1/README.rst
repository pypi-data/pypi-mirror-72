Whatprovides
============

|docs| |license|

.. |docs| image:: https://readthedocs.org/projects/docs/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://docs.readthedocs.io/en/latest/?badge=latest

.. |license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :alt: License
    :scale: 100%
    :target: https://opensource.org/licenses/Apache-2.0


**whatprovides** is a package that allows you to search for python modules that contain declared classes,
functions and variables by the name of the search object.

This is an analogue of the **yum whatprovides** command in **Centos**.

Search is performed in the current active virtual environment.

For example:

 .. code-block:: bash

  whatprovides.py ArgumentParser

Will return something like this:

  class: ArgumentParser: /usr/lib/python3.7/argparse.py

Documentation
-------------

https://whatprovides.readthedocs.io