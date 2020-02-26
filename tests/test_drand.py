import json

from aiohttp import web

from pytest import mark


_distkey = "87c471f7dfb120b04ab749f61a20635f90096dd804c00d06ffe5c0a0a5ba6e43759652a1faa5122880f23b5f6a005bac"
response_distkey = {"key": _distkey}
response_public_rand = {
    "round": 3,
    "previous": "a5d55fbbd2029117188a37c56d368126d2eafe558bba7de536970a650a8f2aa958b84c03cac5af3959886608415f809910df98493756b5855bdcb23de6e6d75117822f689f3d79182a11a408267bd8030354c904be591e649a761c5402c4177f",
    "signature": "89463f52052c02349fe97692ca4de67e5c87160f8731cfd80d2a7587b40d5e7cca1d5e34d0cb7207c287d21023e80a1e01dae8840737623dd389e36faac5641f1fa642909a06e85c6da8de1f620c898e094a38cdd4b1aab5e8d4fe6177a0cfe5",
    "randomness": "bd6d1deec5a7f54ad0aa51d1c871767a337c1e7f23d4b178133523a0a4098247",
}


async def handler_distkey(request):
    text = json.dumps(response_distkey)
    return web.Response(text=text, content_type="application/json")


async def handler_public_rand(request):
    text = json.dumps(response_public_rand)
    return web.Response(text=text, content_type="application/json")


async def test_get_distkey(aiohttp_client, loop):
    from drand.drand import get_distkey

    app = web.Application()
    app.router.add_get("/api/info/distkey", handler_distkey)
    client = await aiohttp_client(app)
    address = f"{client.host}:{client.port}"
    distkey = await get_distkey(address, session=client.session, tls=False)
    assert distkey == response_distkey["key"]


@mark.parametrize("epoch", (None, response_public_rand["round"]))
async def test_get_and_verify(aiohttp_client, loop, epoch):
    from drand.drand import get_and_verify

    app = web.Application()
    path = "/api/public" if epoch is None else f"/api/public/{epoch}"
    app.router.add_get(path, handler_public_rand)
    client = await aiohttp_client(app)
    address = f"{client.host}:{client.port}"
    public_rand = await get_and_verify(
        address, distkey=_distkey, session=client.session, tls=False, round_=epoch
    )
    assert public_rand == response_public_rand
