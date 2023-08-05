Évariste 🍼 Recursively compile and publish a directory tree
============================================================

  On s'empressera de publier ses moindres observations pour peu qu'elles
  soient nouvelles et on ajoutera : « Je ne sais pas le reste. »

  -- Évariste Galois, 1831

.. note::

  As of june 2020, although this project is far less active than I would like (and not documented yet),
  it is still maintained: I use it almost daily.

Example
-------

I use this program to convert `this <https://framagit.org/lpaternault/cours-2-math>`__ (a repository of several hundreds of .tex files, with a few LibreOffice documents) to `that <https://lpaternault.frama.io/cours-2-math/>`__ (a web page representing the same directory structures, with the same files, along with their compiled (pdf) version, and some comments).

What's new?
-----------

See `changelog <https://framagit.org/spalax/evariste/blob/master/CHANGELOG.md>`_.

Download and install
--------------------

* From sources:

  * Download: https://pypi.python.org/pypi/evariste
  * Install (in a `virtualenv`, if you do not want to mess with your distribution installation system)::

        python3 -m pip install .

* From pip::

    pip install evariste

* Quick and dirty Debian (and Ubuntu?) package

  This requires `stdeb <https://github.com/astraw/stdeb>`_ to be installed::

      python3 setup.py --command-packages=stdeb.command bdist_deb
      sudo dpkg -i deb_dist/evariste-<VERSION>_all.deb

Documentation
-------------

* The compiled documentation is available on `readthedocs <http://evariste.readthedocs.io>`_

* To compile it from source, download and run::

      cd doc && make html
