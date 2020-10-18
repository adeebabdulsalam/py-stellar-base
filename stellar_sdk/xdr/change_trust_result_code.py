# This is an automatically generated file.
# DO NOT EDIT or your changes may be overwritten
import base64
from enum import IntEnum
from xdrlib import Packer, Unpacker

from ..__version__ import __issues__
from ..exceptions import ValueError

__all__ = ["ChangeTrustResultCode"]


class ChangeTrustResultCode(IntEnum):
    """
    XDR Source Code
    ----------------------------------------------------------------
    enum ChangeTrustResultCode
    {
        // codes considered as "success" for the operation
        CHANGE_TRUST_SUCCESS = 0,
        // codes considered as "failure" for the operation
        CHANGE_TRUST_MALFORMED = -1,     // bad input
        CHANGE_TRUST_NO_ISSUER = -2,     // could not find issuer
        CHANGE_TRUST_INVALID_LIMIT = -3, // cannot drop limit below balance
                                         // cannot create with a limit of 0
        CHANGE_TRUST_LOW_RESERVE =
            -4, // not enough funds to create a new trust line,
        CHANGE_TRUST_SELF_NOT_ALLOWED = -5 // trusting self is not allowed
    };
    ----------------------------------------------------------------
    """

    CHANGE_TRUST_SUCCESS = 0
    CHANGE_TRUST_MALFORMED = -1
    CHANGE_TRUST_NO_ISSUER = -2
    CHANGE_TRUST_INVALID_LIMIT = -3
    CHANGE_TRUST_LOW_RESERVE = -4
    CHANGE_TRUST_SELF_NOT_ALLOWED = -5

    def pack(self, packer: Packer) -> None:
        packer.pack_int(self.value)

    @classmethod
    def unpack(cls, unpacker: Unpacker) -> "ChangeTrustResultCode":
        value = unpacker.unpack_int()
        return cls(value)

    def to_xdr_bytes(self) -> bytes:
        packer = Packer()
        self.pack(packer)
        return packer.get_buffer()

    @classmethod
    def from_xdr_bytes(cls, xdr: bytes) -> "ChangeTrustResultCode":
        unpacker = Unpacker(xdr)
        return cls.unpack(unpacker)

    def to_xdr(self) -> str:
        xdr_bytes = self.to_xdr_bytes()
        return base64.b64encode(xdr_bytes).decode()

    @classmethod
    def from_xdr(cls, xdr: str) -> "ChangeTrustResultCode":
        xdr = base64.b64decode(xdr.encode())
        return cls.from_xdr_bytes(xdr)

    @classmethod
    def _missing_(cls, value):
        raise ValueError(
            f"{value} is not a valid {cls.__name__}, please upgrade the SDK or submit an issue here: {__issues__}."
        )