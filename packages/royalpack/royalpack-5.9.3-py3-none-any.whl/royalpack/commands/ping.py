import asyncio
from typing import *
import royalnet
import royalnet.commands as rc


class PingCommand(rc.Command):
    name: str = "ping"

    description: str = "Display the status of the Herald network."

    syntax: str = ""

    _targets = ["telegram", "discord", "matrix", "constellation"]

    async def run(self, args: rc.CommandArgs, data: rc.CommandData) -> None:
        await data.reply("📶 Ping...")

        tasks = {}

        for target in self._targets:
            tasks[target] = self.loop.create_task(self.interface.call_herald_event(target, "pong"))

        await asyncio.sleep(10)

        lines = ["📶 [b]Pong![/b]", ""]

        for name, task in tasks.items():
            try:
                print(task.result())
            except (asyncio.CancelledError, asyncio.InvalidStateError):
                lines.append(f"🔴 [c]{name}[/c]")
            else:
                lines.append(f"🔵 [c]{name}[/c]")

        await data.reply("\n".join(lines))
