#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Monero Boost codec, portable binary archive
'''

import binascii

from . import xmrserialize as x
from . import helpers
from .core.versioning import TypeWrapper, VersionDatabase, VersionSetting


_UVARINT_BUFFER = bytearray(1)


async def load_uvarint(reader):
    """
    Monero portable_binary_archive boost integer serialization
    :param reader:
    :return:
    """
    buffer = _UVARINT_BUFFER
    await reader.areadinto(buffer)
    size = buffer[0]
    if size == 0:
        return 0

    negative = size < 0
    size = -size if negative else size
    result = 0
    shift = 0

    if size > 8:
        raise ValueError('Varint size too big: %s' % size)

    # TODO: endianity, rev bytes if needed
    for _ in range(size):
        await reader.areadinto(buffer)
        result += buffer[0] << shift
        shift += 8
    return result if not negative else -result


async def dump_uvarint(writer, n):
    """
    Monero portable_binary_archive boost integer serialization
    :param writer:
    :param n:
    :return:
    """
    buffer = _UVARINT_BUFFER
    if n == 0:
        buffer[0] = 0
        return await writer.awrite(buffer)

    negative = n < 0
    ll = -n if negative else n

    size = 0
    while ll != 0:
        ll >>= 8
        size += 1

    buffer[0] = size
    await writer.awrite(buffer)

    ll = -n if negative else n

    # TODO: endianity, rev bytes if needed
    for _ in range(size):
        buffer[0] = ll & 0xff
        await writer.awrite(buffer)
        ll >>= 8


class ObjectRegistry(object):
    def __init__(self):
        self.db = {}
        self.cur_tr = []

    def __getitem__(self, ver):
        return self.db[ver]

    def __setitem__(self, ver, obj):
        self.db[ver] = obj

    def __len__(self):
        return len(self.db)

    def __contains__(self, item):
        return item in self.db

    def pop_tr(self):
        return self.cur_tr.pop()

    def set_tr(self, tr=None):
        self.cur_tr.append(tr)

    def top_tr(self):
        return self.cur_tr[-1]

    def set_obj(self, obj):
        if not self.is_tracking():
            raise ValueError("No current version")
        self.db[self.top_tr()] = obj
        return self.pop_tr()

    def is_tracking(self):
        return len(self.cur_tr) > 0 and self.top_tr() is not None

    def is_tracked(self):
        return self.is_tracking() and self.top_tr() in self.db

    def get_tracked(self):
        return self[self.top_tr()]


class Archive(x.Archive):
    """
    Boost symmetric serialization archive
    """

    def __init__(self, iobj, writing=True, versions=None, **kwargs):
        super().__init__(iobj, writing, **kwargs)
        self.version_db = VersionDatabase()
        self.version_settings = versions  # type: VersionSetting
        self.registry = ObjectRegistry()
        self.tracker = helpers.Tracker()

    def type_in_db(self, tp, params):
        """
        Determines if type is in the database
        :param tp:
        :return:
        """
        tw = TypeWrapper(tp, params)
        return self.version_db.is_versioned(tw)

    def _cur_version(self, tw, elem=None):
        has_version = False
        if elem:
            relem = x.get_elem(elem)
            if relem and hasattr(relem, 'BOOST_VERSION_CUR'):
                version = getattr(relem, 'BOOST_VERSION_CUR')
                has_version = True

        if not has_version and self.version_settings and tw in self.version_settings:
            version = self.version_settings[tw]

        else:
            version = tw.get_current_version()
        return version

    def is_tracking(self):
        return self.registry.is_tracking()

    def is_tracked(self):
        return self.registry.is_tracked()

    def get_tracked(self):
        obj = self.registry.get_tracked()
        self.pop_track()
        return obj

    def track_obj(self, obj, pred=True):
        if not pred:
            return obj
        if self.is_tracking() and not self.is_tracked():
            self.registry.set_obj(obj)
        else:
            self.pop_track()
        return obj

    def pop_track(self, pred=True):
        if pred:
            self.registry.pop_tr()

    async def get_version(self, tp, params):
        """
        Loads version from the stream / version database
        # TODO: instance vs. tp.

        :param tp:
        :param params:
        :return:
        """
        tw = TypeWrapper(tp, params)
        if not tw.is_versioned():
            # self.registry.set_tr()
            return TypeWrapper.ELEMENTARY_RES

        # If not in the DB, load from archive at current position
        if not self.version_db.is_versioned(tw):
            tr = await load_uvarint(self.iobj)
            ver = await load_uvarint(self.iobj)
            self.version_db.set_version(tw, tr, ver)

        else:
            tr, ver = self.version_db.get_version(tw)

        obj_id = None if tr == 0 else await load_uvarint(self.iobj)
        self.registry.set_tr(obj_id)
        return ver

    async def set_version(self, tp, params, version=None, elem=None):
        """
        Stores version to the stream if not stored yet

        :param tp:
        :param params:
        :param version:
        :param elem:
        :return:
        """
        self.registry.set_tr(None)
        tw = TypeWrapper(tp, params)
        if not tw.is_versioned():
            return TypeWrapper.ELEMENTARY_RES

        # If not in the DB, store to the archive at the current position
        if not self.version_db.is_versioned(tw):
            if version is None:
                version = self._cur_version(tw, elem)

            await dump_uvarint(self.iobj, 0)
            await dump_uvarint(self.iobj, version)
            self.version_db.set_version(tw, 0, version)

        return self.version_db.get_version(tw)[1]

    async def version(self, tp, params, version=None, elem=None):
        """
        Symmetric version management

        :param tp:
        :param params:
        :param version:
        :return:
        """
        if self.writing:
            return await self.set_version(tp, params, version, elem)
        else:
            return await self.get_version(tp, params)

    async def uvarint(self, elem):
        """
        Uvarint
        :param elem:
        :return:
        """
        if self.writing:
            return await dump_uvarint(self.iobj, elem)
        else:
            return await load_uvarint(self.iobj)

    async def uint(self, elem, elem_type, params=None):
        """
        Integer types
        :param elem:
        :param elem_type:
        :param params:
        :return:
        """
        one_b_type = x.is_type(elem_type, (x.Int8, x.UInt8))
        if self.writing:
            return (await x.dump_uint(self.iobj, elem, 1)) if one_b_type else (await dump_uvarint(self.iobj, elem))
        else:
            return (await x.load_uint(self.iobj, 1)) if one_b_type else (await load_uvarint(self.iobj))

    async def unicode_type(self, elem):
        """
        Unicode type
        :param elem:
        :return:
        """
        if self.writing:
            await dump_uvarint(self.iobj, len(elem))
            await self.iobj.awrite(bytes(elem, 'utf8'))

        else:
            ivalue = await load_uvarint(self.iobj)
            if ivalue == 0:
                return ''

            fvalue = bytearray(ivalue)
            await self.iobj.areadinto(fvalue)
            return str(fvalue, 'utf8')

    async def blob(self, elem=None, elem_type=None, params=None):
        """
        Loads/dumps blob
        :return:
        """
        elem_type = elem_type if elem_type else elem.__class__
        version = await self.version(elem_type, params, elem=elem)

        if self.is_tracked():
            return self.get_tracked()

        if hasattr(elem_type, 'boost_serialize'):
            elem = elem_type() if elem is None else elem
            self.pop_track()
            return await elem.boost_serialize(self, elem=elem, elem_type=elem_type, params=params, version=version)

        if self.writing:
            self.pop_track()
            return await self.blob_dump(elem=elem, elem_type=elem_type, params=params)

        else:
            obj = await self.blob_load(elem_type=elem_type, params=params, elem=elem)
            return self.track_obj(obj)

    async def blob_dump(self, elem, elem_type, params=None):
        """
        Dumps blob message to the writer.
        Supports both blob and raw value.

        :param writer:
        :param elem:
        :param elem_type:
        :param params:
        :return:
        """
        elem_is_blob = isinstance(elem, x.BlobType)
        elem_params = elem if elem_is_blob or elem_type is None else elem_type
        data = getattr(elem, x.BlobType.DATA_ATTR) if elem_is_blob else elem

        if len(data) != elem_params.SIZE:
            raise ValueError('Fixed size blob has not defined size: %s, path %s' % (elem_params.SIZE, self.tracker))

        await dump_uvarint(self.iobj, len(elem))
        await self.iobj.awrite(data)

    async def blob_load(self, elem_type, params=None, elem=None):
        """
        Loads blob from reader to the element. Returns the loaded blob.

        :param reader:
        :param elem_type:
        :param params:
        :param elem:
        :return:
        """
        ivalue = await load_uvarint(self.iobj)
        fvalue = bytearray(ivalue)
        await self.iobj.areadinto(fvalue)

        if elem is None:
            return fvalue  # array by default

        elif isinstance(elem, x.BlobType):
            setattr(elem, elem_type.DATA_ATTR, fvalue)
            return elem

        else:
            elem.extend(fvalue)

        return elem

    async def container(self, container=None, container_type=None, params=None):
        """
        Loads/dumps container
        :return:
        """
        # Container versioning is a bit tricky, primitive type containers are not versioned.
        elem_type = x.container_elem_type(container_type, params)
        raw_container = container_is_raw(container_type, params)
        elem_elementary = TypeWrapper.is_elementary_type(elem_type)
        is_versioned = not elem_elementary and not raw_container
        version = None

        if is_versioned:
            version = await self.version(container_type, params, elem=container)
            if self.is_tracked():
                return self.get_tracked()

        if hasattr(container_type, 'boost_serialize'):
            container = container_type() if container is None else container
            self.pop_track(is_versioned)
            return await container.boost_serialize(self, elem=container, elem_type=container_type, params=params, version=version)

        # Container entry version + container
        if self.writing:
            self.pop_track(is_versioned)
            return await self.container_dump(container, container_type, params)
        else:
            obj = await self.container_load(container_type, params=params, container=container)
            return self.track_obj(obj, is_versioned)

    async def container_size(self, container_len=None, container_type=None, params=None):
        """
        Container size
        :param container_len:
        :param container_type:
        :param params:
        :return:
        """
        if hasattr(container_type, 'boost_serialize'):
            raise ValueError('not supported')

        if self.writing:
            await dump_uvarint(self.iobj, container_len)
            if not container_is_raw(container_type, params):
                c_elem = x.container_elem_type(container_type, params)
                c_ver = TypeWrapper(c_elem)
                await dump_uvarint(self.iobj, self._cur_version(c_ver))  # element version

            if container_type.FIX_SIZE and container_len != container_type.SIZE:
                raise ValueError('Fixed size container has not defined size: %s' % container_type.SIZE)

        else:
            raise ValueError('Not supported')

    async def container_val(self, elem, container_type, params=None):
        """
        Single cont value
        :param elem:
        :param container_type:
        :param params:
        :param field_archiver:
        :return:
        """
        if hasattr(container_type, 'boost_serialize'):
            raise ValueError('not supported')

        if self.writing:
            elem_type = params[0] if params else None
            if elem_type is None:
                elem_type = container_type.ELEM_TYPE

            await self.dump_field(elem, elem_type, params[1:] if params else None)

        else:
            raise ValueError('Not supported')

    async def container_dump(self, container, container_type, params=None):
        """
        Dumps container of elements to the writer.

        :param writer:
        :param container:
        :param container_type:
        :param params:
        :param field_archiver:
        :return:
        """
        await self.container_size(len(container), container_type, params)

        elem_type = x.container_elem_type(container_type, params)
        for idx, elem in enumerate(container):
            try:
                self.tracker.push_index(idx)
                await self._dump_field(elem, elem_type, params[1:] if params else None)
                self.tracker.pop()
            except Exception as e:
                raise helpers.ArchiveException(e, tracker=self.tracker) from e

    async def container_load(self, container_type, params=None, container=None):
        """
        Loads container of elements from the reader. Supports the container ref.
        Returns loaded container.

        :param container_type:
        :param params:
        :param container:
        :param field_archiver:
        :return:
        """
        raw_container = container_is_raw(container_type, params)
        c_len = await load_uvarint(self.iobj)
        elem_ver = await load_uvarint(self.iobj) if not raw_container else 0

        # if container and c_len != len(container):
        #     raise ValueError('Size mismatch')

        elem_type = x.container_elem_type(container_type, params)
        res = container if container else []
        for i in range(c_len):
            try:
                self.tracker.push_index(i)
                fvalue = await self._load_field(elem_type,
                                                params[1:] if params else None,
                                                x.eref(res, i) if container else None)
                self.tracker.pop()
            except Exception as e:
                raise helpers.ArchiveException(e, tracker=self.tracker) from e

            if not container:
                res.append(fvalue)
        return res

    async def tuple(self, elem=None, elem_type=None, params=None):
        """
        Loads/dumps tuple
        :return:
        """
        version = await self.version(elem_type, params, elem=elem)
        if self.is_tracked():
            return self.get_tracked()

        if hasattr(elem_type, 'boost_serialize'):
            container = elem_type() if elem is None else elem
            self.pop_track()
            return await container.boost_serialize(self, elem=elem, elem_type=elem_type, params=params, version=version)

        if self.writing:
            self.pop_track()
            return await self.dump_tuple(elem, elem_type, params)
        else:
            obj = await self.load_tuple(elem_type, params=params, elem=elem)
            return self.track_obj(obj)

    async def dump_tuple(self, elem, elem_type, params=None):
        """
        Dumps tuple of elements to the writer.

        :param elem:
        :param elem_type:
        :param params:
        :return:
        """
        if len(elem) != len(elem_type.f_specs()):
            raise ValueError('Fixed size tuple has not defined size: %s' % len(elem_type.f_specs()))

        elem_fields = params[0] if params else None
        if elem_fields is None:
            elem_fields = elem_type.f_specs()
        for idx, elem in enumerate(elem):
            try:
                self.tracker.push_index(idx)
                await self._dump_field(elem, elem_fields[idx], params[1:] if params else None)
                self.tracker.pop()

            except Exception as e:
                raise helpers.ArchiveException(e, tracker=self.tracker) from e

    async def load_tuple(self, elem_type, params=None, elem=None):
        """
        Loads tuple of elements from the reader. Supports the tuple ref.
        Returns loaded tuple.

        :param elem_type:
        :param params:
        :param elem:
        :return:
        """
        elem_fields = params[0] if params else None
        if elem_fields is None:
            elem_fields = elem_type.f_specs()

        if elem and len(elem_fields) != len(elem):
            raise ValueError('Size mismatch')

        res = elem if elem else []
        for i in range(len(elem_fields)):
            try:
                self.tracker.push_index(i)
                fvalue = await self._load_field(elem_fields[i],
                                                params[1:] if params else None,
                                                x.eref(res, i) if elem else None)
                self.tracker.pop()

                if not elem:
                    res.append(fvalue)

            except Exception as e:
                raise helpers.ArchiveException(e, tracker=self.tracker) from e

        return res

    async def variant(self, elem=None, elem_type=None, params=None):
        """
        Loads/dumps variant type
        :param elem:
        :param elem_type:
        :param params:
        :return:
        """
        elem_type = elem_type if elem_type else elem.__class__
        version = await self.version(elem_type, params, elem=elem)

        if self.is_tracked():
            return self.get_tracked()

        if hasattr(elem_type, 'boost_serialize'):
            elem = elem_type() if elem is None else elem
            self.pop_track()
            return await elem.boost_serialize(self, elem=elem, elem_type=elem_type, params=params, version=version)

        if self.writing:
            self.pop_track()
            return await self.dump_variant(elem=elem,
                                           elem_type=elem_type if elem_type else elem.__class__, params=params)
        else:
            obj = await self.load_variant(elem_type=elem_type if elem_type else elem.__class__,
                                          params=params, elem=elem)
            return self.track_obj(obj)

    async def dump_variant(self, elem, elem_type=None, params=None):
        """
        Dumps variant type to the writer.
        Supports both wrapped and raw variant.

        :param writer:
        :param elem:
        :param elem_type:
        :param params:
        :return:
        """
        if isinstance(elem, x.VariantType) or elem_type.WRAPS_VALUE:
            await dump_uvarint(self.iobj, elem.variant_elem_type.VARIANT_CODE)
            await self._dump_field(getattr(elem, elem.variant_elem), elem.variant_elem_type)

        else:
            fdef = elem_type.find_fdef(elem_type.f_specs(), elem)
            vcode = fdef[1].BOOST_VARIANT_CODE if hasattr(fdef[1], 'BOOST_VARIANT_CODE') else fdef[1].VARIANT_CODE
            await dump_uvarint(self.iobj, vcode)
            await self._dump_field(elem, fdef[1])

    async def load_variant(self, elem_type, params=None, elem=None, wrapped=None):
        """
        Loads variant type from the reader.
        Supports both wrapped and raw variant.

        :param reader:
        :param elem_type:
        :param params:
        :param elem:
        :param wrapped:
        :return:
        """
        is_wrapped = (isinstance(elem, x.VariantType) or elem_type.WRAPS_VALUE) if wrapped is None else wrapped
        if is_wrapped:
            elem = elem_type() if elem is None else elem

        tag = await load_uvarint(self.iobj)
        for field in elem_type.f_specs():
            ftype = field[1]
            vcode = ftype.BOOST_VARIANT_CODE if hasattr(ftype, 'BOOST_VARIANT_CODE') else ftype.VARIANT_CODE
            if vcode != tag:
                continue

            fvalue = await self._load_field(ftype, field[2:], elem if not is_wrapped else None)
            if is_wrapped:
                elem.set_variant(field[0], fvalue)
            return elem if is_wrapped else fvalue

        raise ValueError('Unknown tag: %s, path: %s' % (tag, self.tracker))

    async def root(self):
        """
        Root level init
        :return:
        """
        if self.writing:
            await self.iobj.awrite(binascii.unhexlify(b'011673657269616c697a6174696f6e3a3a617263686976650000'))

        else:
            hdr = bytearray(2)
            await self.iobj.areadinto(hdr)
            if hdr != bytearray(b'\x01\x16'):
                raise ValueError('Unsupported header')

            hdr = bytearray(22)
            await self.iobj.areadinto(hdr)
            if hdr != bytearray(b'serialization::archive'):
                raise ValueError('Unrecognized magic header')

            tra = await load_uvarint(self.iobj)
            ver = await load_uvarint(self.iobj)
            if tra != 0:
                raise ValueError('Tracking not supported')

    async def root_message(self, msg, msg_type=None):
        """
        Root-level message. First entry in the archive.
        Archive headers processing

        :return:
        """
        await self.root()
        await self.message(msg, msg_type)

    async def message(self, msg, msg_type=None, use_version=None):
        """
        Loads/dumps message
        :param msg:
        :param msg_type:
        :param use_version:
        :return:
        """
        elem_type = msg_type if msg_type is not None else msg.__class__
        version = await self.version(elem_type, None, elem=msg) if use_version is None else use_version

        if self.is_tracked():
            return self.get_tracked()

        if hasattr(elem_type, 'boost_serialize'):
            msg = elem_type() if msg is None else msg
            self.pop_track(use_version is None)
            return await msg.boost_serialize(self, version=version)

        if self.writing:
            self.pop_track(use_version is None)
            return await self.dump_message(msg, msg_type=msg_type)
        else:
            obj = await self.load_message(msg_type, msg=msg)
            return self.track_obj(obj, use_version is None)

    async def message_field(self, msg, field, fvalue=None):
        """
        Dumps/Loads message field
        :param msg:
        :param field:
        :param fvalue: explicit value for dump
        :return:
        """
        fname, ftype, params = field[0], field[1], field[2:]
        try:
            self.tracker.push_field(fname)
            if self.writing:
                fvalue = getattr(msg, fname, None) if fvalue is None else fvalue
                await self._dump_field(fvalue, ftype, params)

            else:
                await self._load_field(ftype, params, x.eref(msg, fname))

            self.tracker.pop()

        except Exception as e:
            raise helpers.ArchiveException(e, tracker=self.tracker) from e

    async def message_fields(self, msg, fields):
        """
        Load/dump individual message fields
        :param msg:
        :param fields:
        :param field_archiver:
        :return:
        """
        for field in fields:
            try:
                self.tracker.push_field(field[0])
                await self.message_field(msg, field)
                self.tracker.pop()

            except Exception as e:
                raise helpers.ArchiveException(e, tracker=self.tracker) from e

        return msg

    async def dump_message(self, msg, msg_type=None):
        """
        Dumps message to the writer.

        :param msg:
        :param msg_type:
        :return:
        """
        mtype = msg.__class__ if msg_type is None else msg_type
        fields = mtype.f_specs()
        for field in fields:
            await self.message_field(msg=msg, field=field)

    async def load_message(self, msg_type, msg=None):
        """
        Loads message if the given type from the reader.
        Supports reading directly to existing message.

        :param msg_type:
        :param msg:
        :return:
        """
        msg = msg_type() if msg is None else msg
        fields = msg_type.f_specs() if msg_type else msg.__class__.f_specs()
        for field in fields:
            await self.message_field(msg, field)

        return msg

    async def field(self, elem=None, elem_type=None, params=None):
        """
        Archive field
        :param elem:
        :param elem_type:
        :param params:
        :return:
        """
        elem_type = elem_type if elem_type else elem.__class__
        fvalue = None
        if issubclass(elem_type, x.UVarintType):
            fvalue = await self.uvarint(x.get_elem(elem))

        elif issubclass(elem_type, x.IntType):
            fvalue = await self.uint(elem=x.get_elem(elem), elem_type=elem_type, params=params)

        elif issubclass(elem_type, x.BlobType):
            fvalue = await self.blob(elem=x.get_elem(elem), elem_type=elem_type, params=params)

        elif issubclass(elem_type, x.UnicodeType):
            fvalue = await self.unicode_type(x.get_elem(elem))

        elif issubclass(elem_type, x.VariantType):
            fvalue = await self.variant(elem=x.get_elem(elem), elem_type=elem_type, params=params)

        elif issubclass(elem_type, x.ContainerType):  # container ~ simple list
            fvalue = await self.container(container=x.get_elem(elem), container_type=elem_type, params=params)

        elif issubclass(elem_type, x.TupleType):  # tuple ~ simple list
            fvalue = await self.tuple(elem=x.get_elem(elem), elem_type=elem_type, params=params)

        elif issubclass(elem_type, x.MessageType):
            fvalue = await self.message(x.get_elem(elem), msg_type=elem_type)

        else:
            raise TypeError

        return fvalue if self.writing else x.set_elem(elem, fvalue)

    async def dump_field(self, writer, elem, elem_type, params=None):
        assert self.iobj == writer
        return await self.field(elem=elem, elem_type=elem_type, params=params)

    async def load_field(self, reader, elem_type, params=None, elem=None):
        assert self.iobj == reader
        return await self.field(elem=elem, elem_type=elem_type, params=params)

    async def _dump_field(self, elem, elem_type, params=None):
        return await self.field(elem=elem, elem_type=elem_type, params=params)

    async def _load_field(self, elem_type, params=None, elem=None):
        return await self.field(elem=elem, elem_type=elem_type, params=params)


def container_is_raw(container_type, params):
    """
    Returns true if container is statically allocated array
    :param container_type:
    :param params:
    :return:
    """
    return container_type.BOOST_RAW_ARRAY if hasattr(container_type, 'BOOST_RAW_ARRAY') else False

