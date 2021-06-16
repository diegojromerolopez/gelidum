# gelidum

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/gelidum.svg)](https://pypi.python.org/pypi/gelidum/)
[![PyPI version gelidum](https://badge.fury.io/py/gelidum.svg)](https://pypi.python.org/pypi/gelidum/)
[![PyPI status](https://img.shields.io/pypi/status/gelidum.svg)](https://pypi.python.org/pypi/gelidum/)
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

## Major highlights
- **freeze** method creates objects with the same attributes of inputs that cannot be expanded or modified.
- Frozen object creation is thread-safe.

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

#### Basic use
```python
from gelidum import freeze
# inplace=False by default
your_frozen_object = freeze(your_object, inplace=False)

# It doesn't raise an exception, mutable object
your_object.attr1 = new_value

# Raises exception, immutable object
your_frozen_object.attr1 = new_value
```

#### What to do when trying to update an attribute
```python
import logging
from gelidum import freeze

class SharedState(object):
  def __init__(self, count: int):
    self.count = count

shared_state = SharedState(1)
      
# on_update="exception": raises an exception when an update is tried
frozen_shared_state = freeze(shared_state, on_update="exception")
frozen_shared_state.count = 4  # Raises exception

# on_update="warning": shows a warning in console exception when an update is tried
frozen_shared_state = freeze(shared_state, on_update="warning")
frozen_shared_state.count = 4  # Shows a warning in console

# on_update="nothing": does nothing when an update is tried
frozen_shared_state = freeze(shared_state, on_update="nothing")
frozen_shared_state.count = 4  # Does nothing, as this update did not exist

# on_update=<lambda message, *args, **kwargs>: calls the function
# Note the parameters of that function must be message, *args, **kwargs
frozen_shared_state = freeze(
  shared_state,
  on_update=lambda message, *args, **kwargs: logging.warning(message)
)
frozen_shared_state.count = 4  # Calls on_update function and logs in the warning level:
                               # "Can't assign 'count' on immutable instance" 
```


### Freeze input params
Use the decorator freeze_params to freeze the input parameters
and avoid non-intended modifications:
```python
from typing import List
from gelidum import freeze_params

@freeze_params()
def append_to_list(a_list: List, new_item: int):
    a_list.append(new_item)
```
If freeze_params is called without arguments, all input parameters will be frozen.
Otherwise, passing a set of parameters will inform the decorator of which named
parameters must be frozen.

```python
from typing import List
from gelidum import freeze_params

@freeze_params(params={"list1", "list2"})
def concat_lists_in(dest: List, list1: List, list2: List):
    dest = list1 + list2

# Freeze dest, list1 and list2
concat_lists_in([], list1=[1, 2, 3], list2=[4, 5, 6])

# Freeze list1 and list2
concat_lists_in(dest=[], list1=[1, 2, 3], list2=[4, 5, 6])
```

Always use kwargs unless you want to freeze the args params. A good way to enforce this is by making the
function have keyword-only arguments:

```python
from typing import List
from gelidum import freeze_params

@freeze_params(params={"list1", "list2"})
def concat_lists_in(*, dest: List, list1: List, list2: List):
    dest = list1 + list2
```

You can use the **Final typehint from gelidum** to signal that an argument is immutable:

```python
from typing import List
from gelidum import freeze_final, Final

@freeze_final
def concatenate_lists(list1: Final[List], list2: Final[List]):
    return list1 + list2
```

Finally, take in account that all freezing is done in a new object (i.e. freeze with inplace=False).
It makes no sense to freeze a parameter of a function that could be used later, *outside*
said function.

### Check original (i.e. "hot") class
- **get_gelidum_hot_class_name**: returns the name of hot class.
- **get_gelidum_hot_class_module** returns the module reference where the hot class was.

## Limitations
- dict, list, tuple and set cannot be modified inplace although the flag inplace is set.
- file handler attributes are not supported. An exception is raised when trying to freeze
  an object with them
- frozen objects cannot be serialized with [marshal](https://docs.python.org/3/library/marshal.html).

## Dependencies
Packages on pypi gelidum uses:
- [frozendict](https://pypi.org/project/frozendict/)

## Roadmap
- [ ] Freeze only when attributes are modified?
- [ ] Include some RELEASE_NOTES.md with information about
  each release.
- [ ] Make some use-cases with threading/async module (i.e. server)
- [ ] Add version of object when freezing.



## Collaborations
This project is open to collaborations. Make a PR or an issue,
and I'll take a look to it.

## License
[MIT](LICENSE) but if you need any other contact me.
