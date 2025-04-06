# gelidum

![test](https://github.com/diegojromerolopez/gelidum/actions/workflows/test.yml/badge.svg)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/diegojromerolopez/gelidum/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/gelidum.svg)](https://pypi.python.org/pypi/gelidum/)
[![PyPI version gelidum](https://badge.fury.io/py/gelidum.svg)](https://pypi.python.org/pypi/gelidum/)
[![PyPI status](https://img.shields.io/pypi/status/gelidum.svg)](https://pypi.python.org/pypi/gelidum/)
[![PyPI download month](https://img.shields.io/pypi/dm/gelidum.svg)](https://pypi.python.org/pypi/gelidum/)
[![Maintainability](https://api.codeclimate.com/v1/badges/331d7d462e578ce5733e/maintainability)](https://codeclimate.com/github/diegojromerolopez/gelidum/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/331d7d462e578ce5733e/test_coverage)](https://codeclimate.com/github/diegojromerolopez/gelidum/test_coverage)

Freeze your objects in python.

![Gelidum](https://raw.githubusercontent.com/diegojromerolopez/gelidum/main/resources/gelidum.jpg "Gelidum image")

[Public domain photo](https://www.flickr.com/photos/140296773@N07/45771062385) by [Katsujiro Maekawa](https://www.flickr.com/photos/hjppo/)

| Latin | English  |
| -------------------------------------------------------- | -------------------------------------------------------- |
| *Caelum est hieme frigidum et gelidum; myrtos oleas quaeque alia assiduo tepore laetantur, aspernatur ac respuit; laurum tamen patitur atque etiam nitidissimam profert, interdum sed non saepius quam sub urbe nostra necat.* | *In winter the air is cold and frosty: myrtles, olives and all other trees which require constant warmth for them to do well, the climate rejects and spurns, though it allows laurel to grow, and even brings it to a luxuriant leaf. Occasionally, however, it kills it, but that does not happen more frequently than in the neighbourhood of Rome.* |

[The Letters of the Younger Pliny, First Series — Volume 1 by the Younger Pliny](https://www.gutenberg.org/ebooks/3234), translated to English by John Benjamin Firth.

## Introduction
Inspired by the method freeze found in other languages like Javascript,
this package tries to make immutable objects to make it easier avoiding
accidental modifications in your code.

See more comments about this project in this [Show HN](https://news.ycombinator.com/item?id=27507524).

## Major highlights
- **freeze** method creates objects with the same attributes of inputs that cannot be expanded or modified.
- Frozen object creation is thread-safe.
- Structural sharing: any frozen object is shared by all of its user objects. There is no copy
performed, only reference.
- cpython and pypy support.

## How it works
In case of the [builtin types](https://docs.python.org/3/library/stdtypes.html)
(bool, None, int, float, bytes, complex, str) it does nothing, as they are already immutable.

For the list type, a [frozenlist](/gelidum/collections/frozenlist.py) with frozen items is returned.

Tuples are already immutable, so a new tuple with frozen items is returned.

When freezing a set, a [frozenzet](/gelidum/collections/frozenzet.py) of frozen items is returned.

In the case of dicts, freezing one of them creates
a new [frozendict](/gelidum/collections/frozendict.py)
with the keys and frozen values of the original dict.

This package, change the methods \_\_setattr\_\_, \_\_delattr\_\_, \_\_set\_\_,
\_\_setitem\_\_, and \_\_delitem\_\_ of the object argument and all of its attributed recursively,
making them raise an exception if the developer tries to call them to modify
the attributes of the instance.

## How to use it

### Freeze in the same object
```python
from typing import List
from gelidum import freeze

class Dummy(object):
  def __init__(self, attr1: int, attr2: List):
    self.attr1 = attr1
    self.attr2 = attr2

dummy = Dummy(1, [2, 3, 4])
frozen_dummy = freeze(dummy, on_freeze="inplace")
assert(id(dummy) == id(frozen_dummy))

# Both raise exception
new_value = 1
dummy.attr1 = new_value
frozen_dummy.attr1 = new_value

# Both raise exception
new_value_list = [1]
dummy.attr2 = new_value_list
frozen_dummy.attr2 = new_value_list
```

### Freeze in a new object

#### Basic use
```python
from typing import List
from gelidum import freeze

class Dummy(object):
  def __init__(self, attr1: int, attr2: List):
    self.attr1 = attr1
    self.attr2 = attr2

dummy = Dummy(1, [2, 3, 4])
# on_freeze="copy" by default
frozen_dummy = freeze(dummy)
assert(id(dummy) != id(frozen_dummy))

# on_freeze="copy" by default
frozen_object_dummy2 = freeze(dummy, on_freeze="copy")

# It doesn't raise an exception,
# dummy keeps being a mutable object
new_attr1_value = 99
dummy.attr1 = new_attr1_value

# Raises exception,
# frozen_dummy is an immutable object
frozen_dummy.attr1 = new_attr1_value
```

#### Access to original object
##### Passing flag to freezer
If you are freezing custom objects, you can pass the flag `save_original_on_copy` to the freeze method to
ensure you have an attribute original_obj in the frozen method.

```python
from gelidum import freeze

class Dummy(object):
  def __init__(self, attr1: int, attr2: int):
    self.attr1 = attr1
    self.attr2 = attr2

dummy = Dummy(1, 2)
frozen_dummy = freeze(dummy, save_original_on_copy=True)

# We are copying the object and freezing it:
assert(id(dummy) != id(frozen_dummy))
# But we are keeping the original object inside it:
assert(id(dummy) == id(frozen_dummy.original_obj))
```

##### Custom freezer
The parameter on_freeze admits a callable, so you can have
some side effects when freezing objects.

There is a particular callable class that allows
returning the original object:

```python
from gelidum import freeze
from gelidum.on_freeze import OnFreezeOriginalObjTracker

class Dummy(object):
    def __init__(self, value1: int, value2: int):
        self.attr1 = value1
        self.attr2 = value2

dummy = Dummy(value1=1, value2=2)

freezer = OnFreezeOriginalObjTracker()

frozen_dummy = freeze(dummy, on_freeze=freezer)
original_obj = freezer.original_obj

assert(dummy == original_obj)
```

Note that in the earlier case the original object is not frozen
but a copy of it.

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
def concat_lists(dest: List, list1: List, list2: List) -> List:
    dest = list1 + list2
    return dest

# Freeze dest, list1 and list2
concat_lists([], list1=[1, 2, 3], list2=[4, 5, 6])

# Freeze list1 and list2
concat_lists(dest=[], list1=[1, 2, 3], list2=[4, 5, 6])
```

Always use kwargs unless you want to freeze the args params. A good way to enforce this is by making the
function have keyword-only arguments:

```python
from typing import List
from gelidum import freeze_params

@freeze_params(params={"list1", "list2"})
def concat_lists_in(*, dest: List, list1: List, list2: List):
    dest = list1 + list2
    return dest
```

You can use the **Final typehint from gelidum** to signal that an argument is immutable:

```python
from typing import List
from gelidum import freeze_final, Final

@freeze_final
def concatenate_lists(list1: Final[List], list2: Final[List]):
    return list1 + list2
```

Finally, take in account that all freezing is done in a new object (i.e. freeze with on_freeze="copy").
It makes no sense to freeze a parameter of a function that could be used later, *outside*
said function.

### Check original (i.e. "hot") class
- **get_gelidum_hot_class_name**: returns the name of hot class.
- **get_gelidum_hot_class_module** returns the module reference where the hot class was.

## Collections
There are four immutable collections in the gelidum.collections module.

- frozendict
- frozenlist
- frozenzet (frozenset is already a builtin type in Python)

All of these classes can be used to make sure a collection of objects
is not modified. Indeed, when creating a new collection object, you
can pass a custom freeze function, to customize the freezing process
of each of its items, e.g.:

```python
import logging
from gelidum.freeze import freeze
from gelidum.collections import frozenzet
from gelidum.typing import FrozenType
from typing import Any


def my_freeze_func(item: Any) -> FrozenType:
  logging.debug(f"Freezing item {item}")
  return freeze(item, on_update="exception", on_freeze="copy")

frozen_zet = frozenzet([1, 2, 3], freeze_func=my_freeze_func)
```

## Rationale and background information
Inspired by my old work with Ruby on Rails, I decided to create a mechanism to make
objects immutable in Python. The first aim was to do a tool to avoid accidental
modifications on the objects while passing them through an execution flow.

Anyways, as time passed I thought that an implementation of a programming language
with real threading support (i.e. not cpython) could be benefited from this feature.
I know that both cpython and pypy implementations of the Python programming
language have a [GIL](https://en.wikipedia.org/wiki/Global_interpreter_lock) but IronPython
and [Graalpython](https://github.com/oracle/graalpython) don't.
IronPython3 has no support for typehintings yet,
but Graalpython seems to work fine, so more experiments will be coming.

On the other hand, I'm also interested in creating functional data structures
in this package, easing the life of developers that do not want side effects.

It's true that the complexity of Python does not play well with this kind of library.
Thus, Python usually serves as easy interface with native libraries (pandas, numpy, etc.)
However, this project is fun to develop and maybe with the popularity of alternative
implementations of Python some work can be done to improve performance.

More information can be seen in this [Show HN post](https://news.ycombinator.com/item?id=27507524)
and some appreciated feedback of the users of that great community.

## Limitations
- dict, list, tuple and set objects cannot be modified inplace although the flag inplace is set.
- functions:
  - Their attributes will be frozen, nothing related to the actual implementation of the function is modified (i.e. no relation between freezing a function and making it a *pure* function).
  - Cannot be frozen in-place.
- file handler attributes are not supported. An exception is raised when trying to freeze
  an object with them.
- frozen objects cannot be serialized with [marshal](https://docs.python.org/3/library/marshal.html).
- frozen objects cannot be (deep)-copied. This limitation is intended to make structural sharing easier.
- Classes with \_\_slots\_\_:
  - cannot be frozen in-place.
  - will be frozen with a unique class. The frozen class will not be shared by instances of the same class.

## Advice & comments on use
### On_update parameter of freeze function
Use on_update with a callable to store when somebody tried to write in the immutable object:
```python
import datetime
import logging
import threading
from gelidum import freeze


class Dummy(object):
  def __init__(self, attr: int):
    self.attr = attr


class FrozenDummyUpdateTryRecorder:
  LOCK = threading.Lock()
  written_tries = []
  
  @classmethod
  def add_writing_try(cls, message, *args, **kwargs):
    logging.warning(message)
    with cls.LOCK:
      cls.written_tries.append({
        "message": message,
        "args": args,
        "kwargs": kwargs,
        "datetime": datetime.datetime.utcnow()
      })


dummy = Dummy(1)
frozen_dummy = freeze(
    dummy,
    on_update=FrozenDummyUpdateTryRecorder.add_writing_try 
  )
# It will call FrozenDummyUpdateTryRecorder.add_writing_try
# and will continue the execution flow with the next sentence.
frozen_dummy.attr = 4
```

### On_freeze parameter of freeze function
The parameter on_freeze of the function freeze must be a string or a callable.
This parameter informs of what to do with the object that will be frozen.
Should it be the same input object frozen or a copy of it?

If it has a string as parameter, values "inplace" and "copy" are allowed.
A value of "inplace" will make the freeze method to try to freeze the object
as-is, while a value of "copy" will make a copy of the original object and then,
freeze that copy. **These are the recommended parameters**.

On the other hand, the interesting part is to define a custom on_freeze method.
This method must return an object of the same type of the input.
**This returned will be frozen, and returned to the caller of freeze**.

Note this parameter has no interference with the structural sharing of the frozen objects.
Any frozen object that have several references to it will be shared, not copied.

```python
import copy

def on_freeze(self, obj: object) -> object:
    frozen_object = copy.deepcopy(obj)
    # log, copy the original method or do any other
    # custom action in this function
    return frozen_object
```
As seen earlier, there is also the possibility to
pass a callable object. If you would like you can even
define your own on_freeze functions by inheriting
from classes:

- OnFreezeCopier
- OnFreezeIdentityFunc

See some examples in [on_freeze.py](/gelidum/on_freeze.py) file.

## Dependencies
This package has no dependencies.

## Python version support
Minimum version support is 3.9.

The following versions are deprecated and will be removed in the following dates:

| Python version | Support removal date |
|:--------------:|:--------------------:|
|      3.7       |      2025-06-01      |
|      3.8       |      2026-01-01      |
|      3.9       |      2026-06-01      |

## Roadmap
- [x] Freeze only when attributes are modified? 
  Not exactly but structural sharing is used.
- [x] Include immutable collections.
- [ ] [Graalpython](https://github.com/oracle/graalpython) support.
- [ ] Make some use-cases with threading/async module (i.e. server)


## Collaborations
This project is open to collaborations. Make a PR or an issue,
and I'll take a look to it.

## License
[MIT](LICENSE) license, but if you need any other contact me.
