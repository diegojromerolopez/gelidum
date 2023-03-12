from gelidum.package import package_is_installed
from gelidum.collections.frozendict import frozendict  # noqa
from gelidum.collections.frozenlist import frozenlist  # noqa
from gelidum.collections.frozenzet import frozenzet  # noqa
if package_is_installed('numpy'):
    from gelidum.collections.frozenndarray import frozenndarray  # noqa
