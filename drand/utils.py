from hashlib import sha256
from pathlib import Path

import toml

from drand.constants import INT_BYTEORDER, INT_BYTE_LENGTH


def int_to_bytes(int_value):
    return int.to_bytes(int_value, INT_BYTE_LENGTH, byteorder=INT_BYTEORDER)


def hex_to_bytes(hex_value):
    return bytes.fromhex(hex_value)


def construct_message_hash(round_, previous_signature):
    return sha256(int_to_bytes(round_) + hex_to_bytes(previous_signature)).digest()


def construct_url(*, address, endpoint, tls):
    scheme = "https" if tls else "http"
    return f"{scheme}://{address}/{endpoint}"


def parse_toml(toml_file):
    return toml.loads(Path(toml_file).read_text())


def get_addresses_from_group_file(group_file):
    group = parse_toml(group_file)
    return [node["Address"] for node in group["Nodes"]]
