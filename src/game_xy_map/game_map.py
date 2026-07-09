from ..game_data import Unit, none_unit
from dependency.modules._error_handling import MEH

class GameMap:
    def __init__(self, width, height):
        self._map: list[list[Unit]] = [
            [
                none_unit for _ in range(width)
            ] for _ in range(height)
        ]
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
        return self.check_wh(x, y).map(lambda xy: self._map[y][x])

    def get_column(self, x: int) -> MEH[list[Unit]]:
        return self.check_wh(x=x).map(
            lambda wh: [self._map[y][x] for y in range(self.height)]
        )

    def get_row(self, y: int) -> MEH[list[Unit]]:
        return self.check_wh(y=y).map(
            lambda wh: self._map[y]
        )

    def set_unit(self, x: int, y: int, unit: Unit) -> MEH:
        def do_set(_):
            self._map[y][x] = unit

        return self.check_wh(x, y).map(do_set)

    def set_column(self, x: int, units: list[Unit]) -> MEH:
        def do_set(_):
            for y in range(self.height):
                self._map[y][x] = units[y]

        if len(units) != self.height:
            return MEH.unit_err("units len != height")

        return self.check_wh(x=x).map(do_set)

    def set_row(self, y: int, units: list[Unit], is_copy: bool = True) -> MEH:
        def do_set(_):
            self._map[y] = units.copy() if is_copy else units

        if len(units) != self.width:
            return MEH.unit_err("units len != width")

        return self.check_wh(y=y).map(do_set)

