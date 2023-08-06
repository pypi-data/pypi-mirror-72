
telegram_me
===========


.. image:: https://img.shields.io/badge/License-MIT-red.svg
   :target: https://github.com/hearot/telegram_me/blob/v1.0.1/LICENSE
   :alt: License: MIT

.. image:: https://img.shields.io/badge/Developer-@hearot-blue.svg
   :target: https://t.me/hearot
   :alt: Developer: @hearot


A simple scraper for getting information from https://t.me links.

Example
^^^^^^^

.. code-block:: python

   from telegram_me import Link

   link = Link.from_username("Wikisource_Bot")

   print(link.bio)  # Output: A @wiki version for wikisource.org. [...]
   print(link.image)  # Output: https://cdn4.telesco.pe/file/...
   print(link.name)  # Output: Wikisource Search
   print(link.username)  # Output: Wikisource_bot

Installation
^^^^^^^^^^^^

You can install this package by simply using ``pip``\ :

.. code-block::

   pip install telegram_me


Changelog
^^^^^^^^^

..

   See `CHANGELOG.md <https://github.com/hearot/telegram_me/blob/v1.0.1/CHANGELOG.md>`_.
   Find new features in `FEATURES.md <https://github.com/hearot/telegram_me/blob/v1.0.1/FEATURES.md>`_.


Commit messages
^^^^^^^^^^^^^^^

..

   See `Conventional Commits <https://www.conventionalcommits.org>`_.


Versioning
^^^^^^^^^^

..

   See `PEP 440 <https://www.python.org/dev/peps/pep-0440/>`_.


Copyright & License
^^^^^^^^^^^^^^^^^^^


* Copyright (C) 2020 `Hearot <https://github.com/hearot>`_.
* Licensed under the terms of the `MIT License <https://github.com/hearot/telegram_me/blob/v1.0.1/LICENSE>`_.


