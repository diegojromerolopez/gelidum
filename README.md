# gelidum

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Maintainability](https://api.codeclimate.com/v1/badges/331d7d462e578ce5733e/maintainability)](https://codeclimate.com/github/diegojromerolopez/gelidum/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/331d7d462e578ce5733e/test_coverage)](https://codeclimate.com/github/diegojromerolopez/gelidum/test_coverage)

Freeze your objects in python.

| Latin | English  |
| -------------------------------------------------------- | -------------------------------------------------------- |
| *Caelum est hieme frigidum et gelidum; myrtos oleas quaeque alia assiduo tepore laetantur, aspernatur ac respuit; laurum tamen patitur atque etiam nitidissimam profert, interdum sed non saepius quam sub urbe nostra necat.* | *In winter the air is cold and frosty: myrtles, olives and all other trees which require constant warmth for them to do well, the climate rejects and spurns, though it allows laurel to grow, and even brings it to a luxuriant leaf. Occasionally, however, it kills it, but that does not happen more frequently than in the neighbourhood of Rome.* |

[The Letters of the Younger Pliny, First Series — Volume 1 by the Younger Pliny](https://www.gutenberg.org/ebooks/3234), translated to English by John Benjamin Firth.

## Introduction
Inspired by the method freeze found in other languages like Javascript,
this package tries to make immutable objects to make it easier avoid
accidental modifications in your code.

## WARNING
This is an **EXPERIMENTAL** package. Don't use it unless you have checked it
fulfills your use-case safely.

## How it works
In case of the builtin types (int, float, str, etc) it makes nothing, as
they are already immutable.

For the list type, a tuple with frozen items is returned.

Tuples are already immutable, so a new tuple with frozen items is returned.

For sets, frozensets of frozen items are returned.

For dicts, it creates a new [frozendict](https://pypi.org/project/frozendict/)
with the keys and frozen values of the original dict.

This package, change the methods \_\_setattr\_\_, \_\_delattr\_\_, \_\_set\_\_,
\_\_setitem\_\_, \_\_delitem\_\_, and \_\_reversed\_\_.

of the object argument and all of its attributed recursively,
making them raise an exception if the developer tries to call them to modify
the attributes of the instance.

## How to use it

### Freeze in the same object
```python
from gelidum import freeze
your_frozen_object = freeze(your_object, inplace=True)
assert(id(your_frozen_object), id(your_object))

# Both raise exception
your_object.attr1 = new_value
your_frozen_object.attr1 = new_value
```

### Freeze in a new object
```python
from gelidum import freeze
# inplace=False by default
your_frozen_object = freeze(your_object, inplace=False)

# Don't raise exception
your_object.attr1 = new_value

# Raises exception
your_frozen_object.attr1 = new_value
```

## Limitations
- dict, list, tuple and set cannot be modified inplace although the flag inplace is set.

## Dependencies
Right now this package uses
[frozendict](https://pypi.org/project/frozendict/). 

## Collaborations
This project is open to collaborations. Make a PR or an issue and
I'll take a look to it.

## License
[MIT](LICENSE)