from typing import *
from royalnet.constellation.api import *
from royalnet.utils import *
from ..tables import *
from sqlalchemy import func


class ApiDiarioRandomStar(ApiStar):
    path = "/api/diario/random/v1"

    parameters = {
        "get": {
            "amount": "The number of diario entries to get."
        }
    }

    tags = ["diario"]

    async def get(self, data: ApiData) -> JSON:
        """Get random diario entries."""
        DiarioT = self.alchemy.get(Diario)
        try:
            amount = int(data["amount"])
        except ValueError:
            raise InvalidParameterError("'amount' is not a valid int.")
        entries: List[Diario] = await asyncify(
            data.session
                .query(DiarioT)
                .order_by(func.random())
                .limit(amount)
                .all
        )
        if len(entries) < amount:
            raise NotFoundError("Not enough diario entries.")
        return list(map(lambda e: e.json(), entries))
