from .exceptions import EnvvarNameError
from .enums import EnvVarType


class DataEnvVar(object):
    """Represent an environment variable declared as char"""
    def __init__(self, channel, handle, name, size):
        self._channel = channel
        self._handle = handle
        self._name = name  # for debugging only
        self._size = size

    def __eq__(self, other):
        value = self._channel.script_envvar_get_data(self._handle, len=self._size, start=0)
        return bytes(value) == other

    def __len__(self):
        return self._size

    # required in Python 2
    def __ne__(self, other):
        return not self == other

    def __getitem__(self, key):
        if isinstance(key, slice):

            # qqqmac fb:25388, BLB-1104
            # size = key.stop - key.start
            # value = self._channel.script_envvar_get_data(self._handle, len=size, start=key.start)
            # Workaround:
            value = self._channel.script_envvar_get_data(self._handle, len=self._size, start=0)
            value = value[key.start:key.stop]

            if key.step is not None:
                raise NotImplementedError('step is not yet implemented in read')
        else:
            # qqqmac fb:25388, BLB-1104
            # value = self._channel.script_envvar_get_data(self._handle, len=1, start=key)
            # Workaround:
            value = self._channel.script_envvar_get_data(self._handle, len=self._size, start=0)
            value = value[key]

        return value

    def __setitem__(self, key, value):
        if isinstance(key, slice):

            # qqqmac fb:25388, BLB-1104
            # size = key.stop - key.start
            # self._channel.script_envvar_set_data(self._handle, value, len=size, start=key.start)
            # Workaround:
            data = self._channel.script_envvar_get_data(self._handle, len=self._size, start=0)
            pre_data = data[:int(key.start or 0)]
            if key.stop is not None:
                post_data = data[key.stop:]
            else:
                post_data = b''
            data = pre_data + value + post_data
            self._channel.script_envvar_set_data(self._handle, data, len=self._size, start=0)

            if key.step is not None:
                raise NotImplementedError('step is not yet implemented in set')
        else:
            # qqqmac fb:25388, BLB-1104
            # self._channel.script_envvar_set_data(self._handle, value, len=1, start=key)
            data = self._channel.script_envvar_get_data(self._handle, len=self._size, start=0)
            data = data[:key] + value + data[key + 1:]
            self._channel.script_envvar_set_data(self._handle, data, len=self._size, start=0)

    def __str__(self):
        value = self._channel.script_envvar_get_data(self._handle, len=self._size, start=0)
        return value.decode('utf-8')  # qqqmac should we have a proper decode method?


class EnvVar(object):
    """Used to access environment variables"""
    class Attrib(object):
        def __init__(self, handle=None, type_=None, size=None):
            self.handle = handle
            self.type_ = type_
            self.size = size

    def __init__(self, channel):
        self.__dict__['_channel'] = channel
        self.__dict__['_attrib'] = {}

    def _ensure_open(self, name):
        if name.startswith('_'):
            raise EnvvarNameError(name)
        # We just check the handle here
        if name not in self.__dict__['_attrib']:
            self._attrib[name] = EnvVar.Attrib(
                *self._channel.scriptEnvvarOpen(name))

    def __getattr__(self, name):
        self._ensure_open(name)
        handle = self._attrib[name].handle
        if self._attrib[name].type_ == EnvVarType.INT:
            value = self._channel.scriptEnvvarGetInt(handle)
        elif self._attrib[name].type_ == EnvVarType.FLOAT:
            value = self._channel.scriptEnvvarGetFloat(handle)
        elif self._attrib[name].type_ == EnvVarType.STRING:
            size = self._attrib[name].size
            value = DataEnvVar(self._channel, handle, name, size)
        else:
            msg = "getting is not implemented for type {type_}"
            msg = msg.format(type_=self._attrib[name].type_)
            raise TypeError(msg)
        return value

    def __setattr__(self, name, value):
        self._ensure_open(name)
        handle = self._attrib[name].handle
        if self._attrib[name].type_ == EnvVarType.INT:
            value = self._channel.scriptEnvvarSetInt(handle, value)
        elif self._attrib[name].type_ == EnvVarType.FLOAT:
            value = self._channel.scriptEnvvarSetFloat(handle, value)
        elif self._attrib[name].type_ == EnvVarType.STRING:
            size = self._attrib[name].size
            if len(value) != size:
                raise ValueError("Size of data and envvar is not same")
            self._channel.script_envvar_set_data(handle, value, len=size, start=0)
        else:
            msg = "setting is not implemented for type {type_}"
            msg = msg.format(type_=self._attrib[name].type_)
            raise TypeError(msg)
