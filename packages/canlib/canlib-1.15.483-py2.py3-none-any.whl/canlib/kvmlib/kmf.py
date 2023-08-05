from collections import namedtuple
import ctypes as ct

from ..versionnumber import VersionNumber
from .enums import Device
from .log import MountedLog
from .wrapper import dll


def openKmf(path, device_type=Device.MHYDRA_EXT):
    """Open a kmf file from disk

    Arguments:

        path (`str`): The filepath to the .KMF file
            (e.g. ``"data/kmf/LOG00000.KMF"``).

        device_type (`canlib.kvmlib.Device`): The type of the memorator that
            created the .KMF file(s) (defaults to
            `canlib.kvmlib.Device.MHYDRA_EXT`)

    Returns:
        `Kmf`

    .. versionadded:: 1.6

    """
    filename = ct.create_string_buffer(path.encode('utf8'))
    status = ct.c_int()
    major = ct.c_int()
    minor = ct.c_int()
    handle = dll.kvmKmfOpenEx(
        filename, ct.byref(status), device_type, ct.byref(major), ct.byref(minor))

    return Kmf(handle, VersionNumber(major.value, minor.value))


class KmfSystem(object):
    """The base class of `Kmf` and `Memorator`

    The `Kmf` and `Memorator` classes are very similar, they are different ways
    of reading log files (`LogFile`) created by a memorator. This class
    represents the common ground between all ways of accessing log files.

    All subclasses should have a `log` attribute which is an `UnmountedLog` or
    subclass thereof.

    This class automatically closes its internal handle when garbage collected.

    .. versionadded:: 1.6

    """
    DiskUsage = namedtuple('DiskUsage', 'used total')

    def __init__(self, handle):
        self.handle = handle

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __del__(self):
        self.close()

    @property
    def disk_usage(self):
        """`KmfSystem.DiskUsage`: The disk usage

        The tuple has one `used` and one `total` field (in that order), which
        reference disk space in megabytes.

        """
        total = ct.c_uint32()
        used = ct.c_uint32()
        dll.kvmKmfGetUsage(self.handle, ct.byref(total), ct.byref(used))

        # convert to MB
        used = int(used.value * 512) / 10**6
        total = int(total.value * 512) / 10**6
        return self.DiskUsage(used=used, total=total)

    def close(self):
        """Close the internal handle

        Warning:
            This invalidates the object.
        """
        if self.handle is not None:
            dll.kvmClose(self.handle)
            self.handle = None


class Kmf(KmfSystem):
    """A kmf file opened with `kvmlib.openKmf`

    The main use of this class is using its `log` attribute, which is a
    `MountedLog` object (see its documentation for how to use it).

    Also see the base class `kvmlib.KmfSystem` for inherited functionality.

    Attributes:
        log (`MountedLog`): Object representing the log of log files within the
            kmf container-file.

    .. versionadded:: 1.6

    """
    def __init__(self, handle, ldf_version):
        super(Kmf, self).__init__(handle)

        self.log = MountedLog(self, ldf_version)
