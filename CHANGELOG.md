# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## 0.8.0 (2025-04-05)
### Features
- Freezing of functions (i.e. freezing of function attributes).

## 0.7.2 (2025-03-30)
### Fixes
- Improve type hinting support. 
- Check project style with flake8 and black.
- Remove requirements.txt file (this project has no dependencies).
- Deprecation schedule of Python versions:
  - 3.7
  - 3.8
  - 3.9

## 0.7.1 (2024-10-25)
### Fixes
- Add support for cpython 3.13 and pypy 3.10.
- Add pyproject.toml specifying that this package uses setuptools. 

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