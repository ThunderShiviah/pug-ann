pug-ann
=======

|Build Status| |Coverage Status| |Version Status| |Downloads|

Artificial Neural Network (ANN) utilities
-----------------------------------------

This is a namespace package (sub-package) of the pug package a
collection of utilities by and for the PDX Python User Group.

--------------

Introduction
------------

Artificial Neural Network utilities by and for the PDX Python User Group
(PUG).

--------------

Installation
------------

On a Posix System
~~~~~~~~~~~~~~~~~

You really want to contribute, right?

::

    git clone https://github.com/hobson/pug-ann.git

If you're a user and not a developer, and have an up-to-date posix OS
with the postgres, xml2, and xlst development packages installed, then
just use ``pip``.

::

    pip install pug-ann --allow-external pybrain

Fedora
~~~~~~

If you're on Fedora >= 16 but haven't done a lot of python binding
development, then you'll need some libraries before pip will succeed.

::

    sudo yum install -y python-devel libxml2-devel libxslt-devel gcc-gfortran python-scikit-learn postgresql postgresql-server postgresql-libs postgresql-devel
    pip install pug --allow-external pybrain

Bleeding Edge
~~~~~~~~~~~~~

Even the releases are very unstable, but if you want to have the latest,
most broken code

::

    pip install git+git://github.com/hobsonlane/pug.git@master --allow-external pybrain

Warning
~~~~~~~

This software is in alpha testing. Install at your own risk.

--------------

Development
-----------

I love merging PRs and adding contributors to the ``__authors__`` list:

::

    git clone https://github.com/hobson/pug-ann.git

.. |Build Status| image:: https://travis-ci.org/hobson/pug-ann.svg?branch=master
   :target: https://travis-ci.org/hobson/pug-ann
.. |Coverage Status| image:: https://coveralls.io/repos/hobson/pug-ann/badge.png
   :target: https://coveralls.io/r/hobson/pug-ann
.. |Version Status| image:: https://pypip.in/v/pug-ann/badge.png
   :target: https://pypi.python.org/pypi/pug-ann/
.. |Downloads| image:: https://pypip.in/d/pug-ann/badge.png
   :target: https://pypi.python.org/pypi/pug-ann/
