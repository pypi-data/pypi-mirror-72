from typing import *
import royalnet
import royalnet.commands as rc


class PongEvent(rc.Event):
    name = "pong"

    async def run(self, **kwargs) -> dict:
        return {"status": "connected"}
