#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
XMR types
"""

from micropython import const

from apps.monero.xmr.serialize.message_types import BlobType

_c0 = const(0)
_c1 = const(1)
_c32 = const(32)
_c64 = const(64)

#
# cryptonote_basic.h
#


class Hash(BlobType):
    __slots__ = ("data",)
    DATA_ATTR = "data"
    FIX_SIZE = _c1
    SIZE = _c32


class ECKey(BlobType):
    __slots__ = ("bytes",)
    DATA_ATTR = "bytes"
    FIX_SIZE = _c1
    SIZE = _c32


ECPoint = Hash
SecretKey = ECKey
ECPublicKey = ECPoint
KeyImage = ECPoint
KeyDerivation = ECPoint
