import ctypes as ct

from .. import dllLoader
from .. import VersionNumber
from .. import deprecation
from .dll import KvlclibDll

_ct_dll = dllLoader.load_dll(win_name='kvlclib.dll',
                             linux_name='libkvlclib.so')
dll = KvlclibDll(_ct_dll)


@deprecation.deprecated.favour('dllversion')
def getVersion():
    """Get the kvlclib version number as a `str`

    .. deprecated:: 1.5
       Use `dllversion` instead.

    """
    return str(dllversion())


def dllversion():
    """Get the kvlclib version number as a `VersionNumber`"""
    major = ct.c_int()
    minor = ct.c_int()
    build = ct.c_int()
    dll.kvlcGetVersion(
        ct.byref(major), ct.byref(minor), ct.byref(build))
    version = VersionNumber(major.value, minor.value, build.value)
    return version
