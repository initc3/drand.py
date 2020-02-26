from hashlib import sha256

from aiohttp import ClientSession

from py_ecc import bls

from drand.constants import DRAND_DOMAIN, ENDPOINTS
from drand.exceptions import SignatureVerificationFailure, VerificationFailure
from drand.utils import construct_url, int_to_bytes


########################################################################################
#                                                                                      #
#                               Verification functions                                 #
#                                                                                      #
########################################################################################
def verify(*, randomness, signature, message_hash, distkey, domain=DRAND_DOMAIN):
    if not verify_randomness_hash(randomness, signature):
        raise VerificationFailure(
            f"The hash of the signature {signature.hex()} is not equal to "
            f"the randomness value {randomness.hex()}"
        )
    return verify_signature(
        message_hash=message_hash,
        distkey=distkey,
        signature=signature,
        domain=DRAND_DOMAIN,
    )


def verify_randomness_hash(randomness, signature):
    return sha256(signature).digest() == randomness


def verify_signature(*, distkey, message_hash, signature, domain=DRAND_DOMAIN):
    """ """
    return bls.verify(message_hash, distkey, signature, domain)


########################################################################################
#                                                                                      #
#                               Network functions                                      #
#                                                                                      #
########################################################################################
async def _get_json_with_session(url, session):
    if session:
        async with session.get(url) as resp:
            json_resp = await resp.json()
    async with ClientSession() as session:
        async with session.get(url) as resp:
            json_resp = await resp.json()
    return json_resp


async def get_status(address, *, session=None, tls=True):
    url = construct_url(address=address, endpoint=ENDPOINTS.HOME.value, tls=tls)
    json_resp = await _get_json_with_session(url, session)
    return json_resp["status"]


async def get_group_info(address, *, session=None, tls=True):
    url = construct_url(address=address, endpoint=ENDPOINTS.GROUP.value, tls=tls)
    json_resp = await _get_json_with_session(url, session)
    return json_resp


async def get_distkey(address, *, session=None, tls=True):
    url = construct_url(address=address, endpoint=ENDPOINTS.DISTKEY.value, tls=tls)
    json_resp = await _get_json_with_session(url, session)
    return json_resp["key"]


async def _get_public_rand(address, *, distkey=None, round_="", session=None, tls=True):
    endpoint = (
        f"{ENDPOINTS.PUBLIC_RAND.value}/{round_}"
        if round_
        else ENDPOINTS.PUBLIC_RAND.value
    )
    url = construct_url(address=address, endpoint=endpoint, tls=tls)
    json_resp = await _get_json_with_session(url, session)
    return json_resp


async def get_and_verify(address, *, distkey, round_="", session=None, tls=True):
    json_data = await _get_public_rand(
        address, distkey=distkey, round_=round_, session=session, tls=tls
    )
    if not round_:
        round_ = json_data["round"]
    round_ = int_to_bytes(round_)
    previous_signature = bytes.fromhex(json_data["previous"])
    signature = bytes.fromhex(json_data["signature"])
    randomness = bytes.fromhex(json_data["randomness"])
    message_hash = sha256(round_ + previous_signature).digest()
    distkey_bytes = bytes.fromhex(distkey)
    if not verify(
        randomness=randomness,
        message_hash=message_hash,
        signature=signature,
        distkey=distkey_bytes,
    ):
        raise SignatureVerificationFailure(json_data)
    return json_data
