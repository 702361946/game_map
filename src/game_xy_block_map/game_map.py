from typing import Any

from dependency.modules._error_handling import MEH
from ..game_data import Unit
from .block import Block

class GameMap:
    def __init__(self, block_width: int, block_height: int):
        self._map: dict[str, Block] = {}
        """
        ``key``: ``f"{y},{x}"``
        """

        self.block_width: int = block_width
        self.block_height: int = block_height

    def check_existence_block_block_xy(
            self,
            block_x: int = 0,
            block_y: int = 0
    ) -> MEH[tuple[int, int]]:
        if self._map.get(f"{block_y},{block_x}", None) is not None:
            return MEH.unit_ok((block_x, block_y))
        return MEH.unit_err("block len mismatch")

    def check_existence_block_map_xy(
            self,
            x: int = 0,
            y: int = 0
    ) -> MEH[tuple[int, int]]:
        block_x, block_y, *_ = self.map_xy_to_block_xy(x=x, y=y)
        return self.check_existence_block_block_xy(block_x=block_x, block_y=block_y).map(lambda _: (x, y))

    def map_xy_to_block_xy(self, x: int, y: int) -> tuple[int, int, int, int]:
        """

        :param x:
        :param y:
        :return: block_x, block_y, block_width, block_height
        """
        return (
            x // self.block_width,
            y // self.block_height,
            x % self.block_width,
            y % self.block_height
        )

    def get_block(self, block_x: int, block_y: int) -> MEH[Block]:
        """

        :param block_x:
        :param block_y:
        :return:
        """
        # noinspection PyTypeChecker
        return self.check_existence_block_block_xy(
            block_x=block_x,
            block_y=block_y
        ).map(
            lambda _: self._map.get(f"{block_y},{block_x}")
        )

    def get_unit(self, x: int, y: int) -> MEH[Unit]:
        block_x, block_y, block_w, block_h = self.map_xy_to_block_xy(x=x, y=y)
        return self.get_block(
            block_x=block_x, block_y=block_y
        ).bind(
            lambda block: block.get_unit(x=block_w, y=block_h)
        )

    def cover_block(self, block_x: int, block_y: int, data: Block) -> MEH[tuple[int, int]]:
        if data.width != self.block_width or data.height != self.block_height:
            return MEH.unit_err("data width != block width or data height != block height")

        self._map[f"{block_y},{block_x}"] = data
        return MEH.unit_ok((block_x, block_y,))

    def pop_block(self, block_x: int, block_y: int, default: Any = None) -> MEH[Block | Any]:
        return MEH.unit_ok(self._map.pop(f"{block_y},{block_x}", default))

    def uninstall_block(self, block_x: int, block_y: int) -> MEH[tuple[int, int]]:
        self._map.pop(f"{block_y},{block_x}", None)
        return MEH.unit_ok((block_x, block_y,))
