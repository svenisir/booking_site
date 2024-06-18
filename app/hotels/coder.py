from typing import Any

from fastapi_cache.coder import Coder


class PydanticJsonCoder(Coder):

    @classmethod
    def encode(cls, value: Any) -> str:
        pass
