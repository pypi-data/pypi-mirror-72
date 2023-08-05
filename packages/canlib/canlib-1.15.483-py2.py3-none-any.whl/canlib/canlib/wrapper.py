import ctypes as ct
import struct
import sys
import logging

from .. import dllLoader
from .. import deprecation
from .. import BetaVersionNumber, VersionNumber
from .dll import CanlibDll
from .enums import VersionEx
from . import constants as const


_ct_dll = dllLoader.load_dll(win_name='canlib32.dll',
                             linux_name='libcanlib.so')
dll = CanlibDll(_ct_dll)
dll.canInitializeLibrary()


class bitrateSetting(object):
    """
    Class that holds bitrate setting.

    Attributes:
        freq: Bitrate in bit/s.
        tseg1: Number of quanta from (but not including) the Sync Segment to
            the sampling point.
        tseg2: Number of quanta from the sampling point to the end of the bit.
        sjw: The Synchronization Jump Width, can be 1,2,3, or 4.
        nosamp: The number of sampling points, only 1 is supported.
        syncMode: Unsupported and ignored.
    """

    def __init__(self, freq=1000000, tseg1=4, tseg2=3, sjw=1, nosamp=1,
                 syncMode=0):
        self.freq = freq
        self.tseg1 = tseg1
        self.tseg2 = tseg2
        self.sjw = sjw
        self.nosamp = nosamp
        self.syncMode = syncMode

    def __eq__(self, other):
        if self.freq != other.freq:
            return False
        if self.tseg1 != other.tseg1:
            return False
        if self.tseg2 != other.tseg2:
            return False
        if self.sjw != other.sjw:
            return False
        if self.nosamp != other.nosamp:
            return False
        if self.syncMode != other.syncMode:
            return False
        return True

    # required in Python 2
    def __ne__(self, other):
        return not self == other

    def __str__(self):
        txt = "freq    : %8d\n" % self.freq
        txt += "tseg1   : %8d\n" % self.tseg1
        txt += "tseg2   : %8d\n" % self.tseg2
        txt += "sjw     : %8d\n" % self.sjw
        txt += "nosamp  : %8d\n" % self.nosamp
        txt += "syncMode: %8d\n" % self.syncMode
        return txt


class CANLib(object):
    """Deprecated wrapper class for the Kvaser CANlib.

    .. deprecated:: 1.5

    All functionality of this class has been moved to the canlib module itself::

      # deprecated
      from canlib import canlib
      cl = canlib.CANLib()  # or canlib.canlib()
      cl.functionName()

      # use this instead
      from canlib import canlib
      canlib.functionName()

    """
    dll = dll

    def __init__(self):
        deprecation.manual_warn(
            "Creating CANLib objects is deprecated, "
            "all functionality has been moved to the canlib module itself.")
        # since=1.5
        self._module = sys.modules[__name__]

    def __getattr__(self, name):
        try:
            return getattr(self._module, name)
        except AttributeError:
            raise AttributeError("{t} object has no attribute {n}".format(
                t=str(type(self)), n=name))

    def openChannel(self, channel, flags=0):
        from .channel import openChannel
        return openChannel(channel, flags)


def getErrorText(error_code):
    """Return error text for supplied error_code"""
    msg = ct.create_string_buffer(80)
    dll.canGetErrorText(error_code, msg, ct.sizeof(msg))
    return msg.value.decode()


@deprecation.deprecated.favour('dllversion')
def getVersion():
    """Get the CANlib DLL version number as a `str`

    .. deprecated:: 1.5
       Use `dllversion` instead.

    """
    return str(dllversion())


def _version_number(v, beta):
    """Return `VersionNumber` or `BetaVersionNumber` of v"""
    # assuming byte order 'little':
    if beta:
        version = BetaVersionNumber(major=v >> 8, minor=v & 0xff)
    else:
        version = VersionNumber(major=v >> 8, minor=v & 0xff)
    return version


def enumerate_hardware():
    """Enumerate connected Kvaser devices and rebuild list of available channels

    Returns the number of CAN channels appended.

    .. versionadded:: 1.13

    """
    chan_count = ct.c_int()
    dll.canEnumHardwareEx(ct.byref(chan_count))
    return chan_count.value


def dllversion():
    """Get the CANlib DLL version number

    Args:
        None

    Returns a `BetaVersionNumber` if the CANlib DLL is marked as beta
    (preview), otherwise returns `VersionNumber`.

    .. versionchanged:: 1.6

    """
    try:
        v = dll.canGetVersionEx(VersionEx.VERSION)
    except NotImplementedError:
        # Backward compatibility with CANlib v5.22
        v = dll.canGetVersion()
        return _version_number(v, beta=False)
    beta = dll.canGetVersionEx(VersionEx.BETA)
    return _version_number(v, beta)


def prodversion():
    """Get the CANlib Product version number

    Args:
        None

    Returns a `BetaVersionNumber` if the CANlib driver/DLL is marked as beta
    (preview), otherwise returns `VersionNumber`.

    .. versionadded:: 1.6

    """
    v = dll.canGetVersionEx(VersionEx.PRODVER)
    beta = dll.canGetVersionEx(VersionEx.BETA)
    return _version_number(v, beta)


def getNumberOfChannels(driver=False):
    """Get number of available CAN channels.

    Returns the number of available CAN channels in the computer. The
    virtual channels are included in this number.

    Args:
        None

    Returns:
        chanCount (int): Number of available CAN channels

    """
    chanCount = ct.c_int()
    dll.canGetNumberOfChannels(chanCount)
    return chanCount.value


@deprecation.deprecated.favour("ChannelData(channel).channel_flags")
def getChannelData_Channel_Flags(channel):
    """Get channel status flags

    .. deprecated:: 1.5
       Use `ChannelData` and their ``channel_flags`` attribute instead.

    Returns a :py:class:`ChannelData_Channel_Flags` object holding
    information about the channel.

    Note: Currently not implemented!

    """
    buf = ct.c_uint32()
    dll.canGetChannelData(
        channel,
        const.canCHANNELDATA_CHANNEL_FLAGS,
        ct.byref(buf),
        ct.sizeof(buf),
    )
    flags = ChannelData_Channel_Flags()
    flags.asbyte = buf.value
    return flags


@deprecation.deprecated.favour("ChannelData(channel).device_name")
def getChannelData_Name(channel):
    """Get the product name.

    .. deprecated:: 1.5
       Use `ChannelData` and their ``device_name`` attribute instead.

    Retrieves the product name of the device connected to channel. The name
    is returned as a string.

    Args:
        channel (int): The channel you are interested in

    Returns:
        product_name (string): The product name

    """
    name = ct.create_string_buffer(80)
    dll.canGetChannelData(
        channel,
        const.canCHANNELDATA_DEVDESCR_ASCII,
        ct.byref(name),
        ct.sizeof(name),
    )
    buf_type = ct.c_uint * 1
    buf = buf_type()
    dll.canGetChannelData(
        channel,
        const.canCHANNELDATA_CHAN_NO_ON_CARD,
        ct.byref(buf),
        ct.sizeof(buf),
    )
    return "%s (channel %d)" % (name.value.decode(), buf[0])


@deprecation.deprecated.favour("ChannelData(channel).custom_name")
def getChannelData_Cust_Name(channel):
    """Get the customized channel name.

    .. deprecated:: 1.5
       Use `ChannelData` and their ``custom_name`` attribute instead.

    Retrieves the customized device channel name of the device connected to
    channel. The name is returned as a string.

    Args:
        channel (int): The channel you are interested in

    Returns:
        custom_name (string): The customized device channel name

    """

    name = ct.create_string_buffer(40)
    dll.canGetChannelData(
        channel,
        const.canCHANNELDATA_CUST_CHANNEL_NAME,
        ct.byref(name),
        ct.sizeof(name),
    )
    return "%s" % (name.value.decode())


@deprecation.deprecated.favour("ChannelData(channel).chan_no_on_card")
def getChannelData_Chan_No_On_Card(channel):
    """Get the channel number on the card.

    .. deprecated:: 1.5
       Use `ChannelData` and their ``chan_no_on_card`` attribute instead.

    Retrieves the channel number, as numbered locally on the card, device
    connected to channel.

    Args:
        channel (int): The channel you are interested in

    Returns:
        number (int): The local channel number

    """
    number = ct.c_ulong()
    dll.canGetChannelData(
        channel,
        const.canCHANNELDATA_CHAN_NO_ON_CARD,
        ct.byref(number),
        ct.sizeof(number),
    )
    buf_type = ct.c_uint * 1
    buf = buf_type()
    dll.canGetChannelData(
        channel,
        const.canCHANNELDATA_CHAN_NO_ON_CARD,
        ct.byref(buf),
        ct.sizeof(buf),
    )
    return number.value


@deprecation.deprecated.favour("ChannelData(channel).card_number")
def getChannelData_CardNumber(channel):
    """Get the card number

    .. deprecated:: 1.5
       Use `ChannelData` and their ``card_number`` attribute instead.

    Retrieves the card's number in the computer. Each card type is numbered
    separately. For example, the first PCIEcan card in a machine will have
    number 0, the second PCIEcan number 1, etc.

    Args:
        channel (int): The channel you are interested in

    Returns:
        card_number (int): The device's card number

    """
    buf_type = ct.c_ulong
    buf = buf_type()
    dll.canGetChannelData(
        channel,
        const.canCHANNELDATA_CARD_NUMBER,
        ct.byref(buf),
        ct.sizeof(buf),
    )
    return buf.value


@deprecation.deprecated.favour("ChannelData(channel).card_upc_no")
def getChannelData_EAN(channel):
    """Get EAN code

    .. deprecated:: 1.5
       Use `ChannelData` and their ``card_upc_no`` attribute instead.

    Retrieves the EAN number for the device connected to channel. If there
    is no EAN number, "00-00000-00000-0" will be returned.

    Args:
        channel (int): The channel you are interested in

    Returns:
        ean (str): The device's EAN number

    """
    buf_type = ct.c_uint32 * 2
    buf = buf_type()
    dll.canGetChannelData(
        channel,
        const.canCHANNELDATA_CARD_UPC_NO,
        ct.byref(buf),
        ct.sizeof(buf),
    )
    (ean_lo, ean_hi) = struct.unpack('II', buf)
    return "%02x-%05x-%05x-%x" % (ean_hi >> 12,
                                  ((ean_hi & 0xfff) << 8) | (ean_lo >> 24),
                                  (ean_lo >> 4) & 0xfffff, ean_lo & 0xf)


@deprecation.deprecated
def getChannelData_EAN_short(channel):
    """Get short EAN code

    .. deprecated:: 1.5
       Use `ChannelData` and their ``.card_upc_no.product()`` instead.

    Retrieves the short EAN number, aka product number, for the device
    connected to channel. If there is no EAN number, "00000-0" will be
    returned.

    Args:
        channel (int): The channel you are interested in

    Returns:
        ean (str): The device's shortened EAN number

    """
    buf_type = ct.c_uint32 * 2
    buf = buf_type()
    dll.canGetChannelData(
        channel,
        const.canCHANNELDATA_CARD_UPC_NO,
        ct.byref(buf),
        ct.sizeof(buf),
    )
    (ean_lo, ean_hi) = struct.unpack('II', buf)
    return "%04x-%x" % ((ean_lo >> 4) & 0xffff, ean_lo & 0xf)


@deprecation.deprecated.favour("ChannelData(channel).card_serial_no")
def getChannelData_Serial(channel):
    """Get device serial number

    .. deprecated:: 1.5
       Use `ChannelData` and their ``card_serial_no`` attribute instead.

    Retrieves the serial number for the device connected to channel. If the
    device does not have a serial number, 0 is returned.

    Args:
        channel (int): The channel you are interested in

    Returns:
        serial (int): The device serial number

    """
    buf_type = ct.c_uint32 * 2
    buf = buf_type()
    dll.canGetChannelData(
        channel,
        const.canCHANNELDATA_CARD_SERIAL_NO,
        ct.byref(buf),
        ct.sizeof(buf),
    )
    (serial_lo, serial_hi) = struct.unpack('II', buf)
    # serial_hi is always 0
    return serial_lo


@deprecation.deprecated.favour("ChannelData(channel).driver_name")
def getChannelData_DriverName(channel):
    """Get device driver name

    .. deprecated:: 1.5
       Use `ChannelData` and their ``driver_name`` attribute instead.

    Retrieves the name of the device driver (e.g. "kcany") for the device
    connected to channel. The device driver names have no special meanings
    and may change from a release to another.

    Args:
        channel (int): The channel you are interested in

    Returns:
        driver_name (str): The device driver name

    """
    name = ct.create_string_buffer(80)
    dll.canGetChannelData(
        channel,
        const.canCHANNELDATA_DRIVER_NAME,
        ct.byref(name),
        ct.sizeof(name),
    )
    return name.value.decode()


@deprecation.deprecated.favour("ChannelData(channel).card_firmware_rev")
def getChannelData_Firmware(channel):
    """Get device firmware version

    .. deprecated:: 1.5
       Use `ChannelData` and their ``card_firmware_rev`` attribute instead.

    Retrieves the firmvare version numbers for the device connected to
    channel.

    Args:
        channel (int): The channel you are interested in

    Returns:
        (fw_major, fw_minor, fw_build): The version number

    """
    buf_type = ct.c_ushort * 4
    buf = buf_type()
    dll.canGetChannelData(
        channel,
        const.canCHANNELDATA_CARD_FIRMWARE_REV,
        ct.byref(buf),
        ct.sizeof(buf),
    )
    (build, release, minor, major) = struct.unpack('HHHH', buf)
    return (major, minor, build)


def translateBaud(freq):
    """Translate bitrate constant

    This function translates the canBITRATE_xxx constants to their
    corresponding bus parameter values.

    Args:
        freq: Any of the predefined constants canBITRATE_xxx

    Returns:
        A bitrateSetting object containing the actual values of
            frequency, tseg1, tseg2 etc.

    """
    freq_p = ct.c_long(freq)
    tseg1_p = ct.c_uint()
    tseg2_p = ct.c_uint()
    sjw_p = ct.c_uint()
    nosamp_p = ct.c_uint()
    syncMode_p = ct.c_uint()
    dll.canTranslateBaud(
        ct.byref(freq_p),
        ct.byref(tseg1_p),
        ct.byref(tseg2_p),
        ct.byref(sjw_p),
        ct.byref(nosamp_p),
        ct.byref(syncMode_p),
    )
    rateSetting = bitrateSetting(
        freq=freq_p.value,
        tseg1=tseg1_p.value,
        tseg2=tseg2_p.value,
        sjw=sjw_p.value,
        nosamp=nosamp_p.value,
        syncMode=syncMode_p.value,
    )
    return rateSetting


def unloadLibrary():
    """Unload CANlib

    Unload canlib and release all internal handles.

    Warning:

        Calling `unloadLibrary` invalidates every canlib-object. Use at your
        own risk.

    """
    try:
        dll.canUnloadLibrary()
    except AttributeError as e:
        logging.debug(str(e) + ' (Not implemented in Linux)')


def initializeLibrary():
    """Initialize CANlib library

    Note:

        This initializes the driver and must be called before any other
        function in the CANlib DLL is used. This is handled in most cases by
        the Python wrapper but if you want to trigger a re-enumeration of
        connected devices, call this function.

    Any errors encountered during library initialization will be "silent"
    and an appropriate error code will be returned later on when an API
    call that requires initialization is called.

    """
    dll.canInitializeLibrary()


def reinitializeLibrary():
    """Reinitializes the CANlib driver.

    Convenience function that calls `unloadLibrary` and `initializeLibrary`
    in succession.

    """
    unloadLibrary()
    dll.canInitializeLibrary()


class ChannelData_Channel_Flags_bits(ct.LittleEndianStructure):
    """Access flags of :py:class:`ChannelData_Channel_Flags`

    .. deprecated:: 1.5

    Gives access to individual parts in :py:class:`ChannelData_Channel_Flags`
    as flags.
    """
    _fields_ = [
        ("is_exclusive", ct.c_uint32, 1),
        ("is_open", ct.c_uint32, 1),
        ("is_canfd", ct.c_uint32, 1),
    ]


class ChannelData_Channel_Flags(ct.Union):
    """Holds data from :py:meth:`canlib.getChannelData_Channel_Flags()`

    .. deprecated:: 1.5

    Data in this object may be accessed as an c_uint32 using `object.asbyte`,
    or as indivisual flags using the class
    :py:class:`ChannelData_Channel_Flags_bits`.

    """
    _fields_ = [("b", ChannelData_Channel_Flags_bits),
                ("asbyte", ct.c_uint32)]
