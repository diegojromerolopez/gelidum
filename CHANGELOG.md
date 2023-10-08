# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## 0.7.0 (2023-10-08)
### Features
- Adding `original_obj` attribute to **frozen by copying objects** to get the original object.
  This original_obj attribute is only present in frozen objects, not in their attributes even if they are objects, e.g.
  ```python
  from gelidum import freeze
  
  class DummyChild(object):
    def __init__(self, value: int):
        self.attr = value

  class Dummy(object):
      def __init__(self, child: DummyChild):
          self.child = child

  dummy_child = DummyChild(value=1)
  dummy = Dummy(child=dummy_child)
  frozen_dummy = freeze(dummy, on_freeze="copy")

  assert(frozen_dummy.original_obj.__class__ == dummy.__class__)
  assert(id(frozen_dummy.original_obj) == id(dummy))
  assert(frozen_dummy.child.original_obj == None)
  ```
### Fixes
- Include support for python 3.12.
- Add cpython 3.12 to CI.

## 0.6.0 (2023-03-12)
### Features
- Beta support for freezing [numpy arrays](https://numpy.org/doc/stable/reference/arrays.html).

## 0.5.9 (2023-01-01)
### Features
- Allow freezing of objects whose class has \_\_slots\_\_.