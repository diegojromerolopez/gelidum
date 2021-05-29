# freeze
Freeze your objects in python


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

For the list type, a tuple is returned.

For sets, frozensets are returned.

For dicts, it creates a new [frozendict](https://pypi.org/project/frozendict/)
with the keys and values of the original dict.

This package, change the methods \_\_setattr\_\_, \_\_delattr\_\_, \_\_set\_\_
of the object argument and all of its attributed recursively,
making them raise an exception if the developer tries to call them to modify
the attributes of the instance.

## How to use it
```python
from freeze import freeze
your_frozen_object = freeze(your_object)

# Raises exception
your_frozen_object.attr1 = new_value
```

## Limitations
- hash issues are completely ignored for now.
- this library does not modify the object but creates a new
one with the same content by frozen.

## Dependencies
Right now this package uses
[frozendict](https://pypi.org/project/frozendict/). 


## License
MIT