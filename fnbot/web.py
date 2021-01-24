import asyncio
from sanic import Sanic
from sanic.response import json

app = Sanic("fnbot")


@app.route('/')
async def test(request):
    return json({'hello': 'world'})


async def setup():
    app.run(host='0.0.0.0', port=8000)


