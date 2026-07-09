from ..game_data import none_unit, Unit
from dependency.modules._error_handling import MEH

class Block:
    """
    因为tuple不可变,所以每一次set都会重建区块,请小心调用
    """
    def __init__(self, width: int, height: int):
        self._block: tuple[tuple[Unit, ...], ...] = tuple(
            tuple(none_unit for _ in range(width))
            for _ in range(height)
        )
        """
        y, x
        """

        self.width: int = width
        self.height: int = height

    def check_wh(self, x: int = 0, y: int = 0) -> MEH[tuple[int, int]]:
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return MEH.unit_err("x or y out of range")
        return MEH.unit_ok((x, y))

    def get_unit(self, x: int, y: int) -> MEH[Unit]:
        return self.check_wh(x, y).map(lambda xy: self._block[y][x])

    def get_column(self, x: int) -> MEH[tuple[Unit, ...]]:
        return self.check_wh(x=x).map(
            lambda wh: tuple([self._block[y][x] for y in range(self.height)])
        )

    def get_row(self, y: int) -> MEH[tuple[Unit, ...]]:
        return self.check_wh(y=y).map(
            lambda wh: self._block[y]
        )

    def set_unit(self, x: int, y: int, unit: Unit) -> MEH:
        # noinspection PyUnusedLocal
        def do_set(xy):
            new_row = list(self._block[y])
            new_row[x] = unit
            self._block = tuple(
                tuple(new_row) if i == y else self._block[i]
                for i in range(self.height)
            )

        return self.check_wh(x, y).map(do_set)

    def set_column(self, x: int, units: tuple[Unit, ...]) -> MEH:
        # noinspection PyUnusedLocal
        def do_set(xy):
            self._block = tuple(
                tuple(
                    units[y] if col == x else self._block[y][col]
                    for col in range(self.width)
                )
                for y in range(self.height)
            )

        if len(units) != self.height:
            return MEH.unit_err("units len != height")

        return self.check_wh(x=x).map(do_set)

    def set_row(
            self,
            y: int,
            units: tuple[Unit, ...],
            is_copy: bool = True
    ) -> MEH:
        # noinspection PyUnusedLocal
        def do_set(xy):
            row = tuple(units) if is_copy else units
            self._block = tuple(
                row if i == y else self._block[i]
                for i in range(self.height)
            )

        if len(units) != self.width:
            return MEH.unit_err("units len != width")
        return self.check_wh(y=y).map(do_set)

    @classmethod
    def up_block(
            cls,
            width: int,
            height: int,
            data: tuple[tuple[Unit, ...], ...],
    ) -> MEH[Block]:
        if len(data) != height:
            return MEH.unit_err("data height != block height")
        for i in range(height):
            if len(data[i]) != width:
                return MEH.unit_err(
                    f"data existence width != block width, from {i}"
                )
            for _i in range(width):
                if not isinstance(data[i][_i], Unit):
                    return MEH.unit_err(
                        f"data existence width != block width, from {i}:{_i}"
                    )

        block = cls(width, height)
        block._block = data
        return MEH.unit_ok(block)



