gelidum
=======

Freeze your objects in python.

+-----------------------------------+-----------------------------------+
| Latin                             | English                           |
+===================================+===================================+
| *Caelum est hieme frigidum et     | *In winter the air is cold and    |
| gelidum; myrtos oleas quaeque     | frosty: myrtles, olives and all   |
| alia assiduo tepore laetantur,    | other trees which require         |
| aspernatur ac respuit; laurum     | constant warmth for them to do    |
| tamen patitur atque etiam         | well, the climate rejects and     |
| nitidissimam profert, interdum    | spurns, though it allows laurel   |
| sed non saepius quam sub urbe     | to grow, and even brings it to a  |
| nostra necat.*                    | luxuriant leaf. Occasionally,     |
|                                   | however, it kills it, but that    |
|                                   | does not happen more frequently   |
|                                   | than in the neighbourhood of      |
|                                   | Rome.*                            |
+-----------------------------------+-----------------------------------+

`The Letters of the Younger Pliny, First Series — Volume 1 by the
Younger Pliny <https://www.gutenberg.org/ebooks/3234>`__, translated to
English by John Benjamin Firth.

Introduction
------------

Inspired by the method freeze found in other languages like Javascript,
this package tries to make immutable objects to make it easier avoid
accidental modifications in your code.

WARNING
-------

This is an **EXPERIMENTAL** package. Don’t use it unless you have
checked it fulfills your use-case safely.

How it works
------------

In case of the builtin types (int, float, str, etc) it makes nothing, as
they are already immutable.

For the list type, a tuple with frozen items is returned.

Tuples are already immutable, so a new tuple with frozen items is
returned.

For sets, frozensets of frozen items are returned.

For dicts, it creates a new
`frozendict <https://pypi.org/project/frozendict/>`__ with the keys and
frozen values of the original dict.

This package, change the methods \__setattr__, \__delattr__, \__set__,
\__setitem__, \__delitem__, and \__reversed__.

of the object argument and all of its attributed recursively, making
them raise an exception if the developer tries to call them to modify
the attributes of the instance.

How to use it
-------------

Freeze in the same object
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   from gelidum import freeze
   your_frozen_object = freeze(your_object, inplace=True)
   assert(id(your_frozen_object), id(your_object))

   # Both raise exception
   your_object.attr1 = new_value
   your_frozen_object.attr1 = new_value

Freeze in a new object
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   from gelidum import freeze
   # inplace=False by default
   your_frozen_object = freeze(your_object, inplace=False)

   # Don't raise exception
   your_object.attr1 = new_value

   # Raises exception
   your_frozen_object.attr1 = new_value

Freeze input params
~~~~~~~~~~~~~~~~~~~

Use the decorator freeze_params to freeze the input parameters and avoid
non-intended modifications:

.. code:: python

   from typing import List
   from gelidum import freeze_params

   @freeze_params()
   def append_to_list(a_list: List, new_item: int):
       a_list.append(new_item)

If freeze_params is called without arguments, all input parameters will
be frozen. Otherwise, passing a set of parameters will inform the
decorator of which parameters must be frozen.

Take in account that all freezing is done in a new object (i.e. freeze
with inplace=False). It makes no sense to freeze a parameter of a
function that could be used later, *outside* said function.

Limitations
-----------

-  dict, list, tuple and set cannot be modified inplace although the
   flag inplace is set.
-  file handler attributes are not supported.

Dependencies
------------

Right now this package uses
`frozendict <https://pypi.org/project/frozendict/>`__.

Roadmap
-------

-  [ ] Make pypi package.
-  [ ] Measure cost in time of freezing objects.
-  [ ] Check that pickle serialization works fine.
-  [ ] Add delayed_freeze, a function that freezes an object but when a
   condition happens.

Collaborations
--------------

This project is open to collaborations. Make a PR or an issue, and I’ll
take a look to it.

License
-------

`MIT <LICENSE>`__

.. |License| image:: https://img.shields.io/badge/License-MIT-blue.svg
   :target: https://opensource.org/licenses/MIT
.. |Maintenance| image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
   :target: https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity
.. |made-with-python| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
   :target: https://www.python.org/
.. |Maintainability| image:: https://api.codeclimate.com/v1/badges/331d7d462e578ce5733e/maintainability
   :target: https://codeclimate.com/github/diegojromerolopez/gelidum/maintainability
.. |Test Coverage| image:: https://api.codeclimate.com/v1/badges/331d7d462e578ce5733e/test_coverage
   :target: https://codeclimate.com/github/diegojromerolopez/gelidum/test_coverage
