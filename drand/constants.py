from enum import Enum


DRAND_DOMAIN = bytes([1, 9, 6, 9, 9, 6, 9, 2])

INT_BYTE_LENGTH = 8
INT_BYTEORDER = "big"


class ENDPOINTS(Enum):
    HOME = "api"
    PUBLIC_RAND = "api/public"
    DISTKEY = "api/info/distkey"
    GROUP = "api/info/group"
