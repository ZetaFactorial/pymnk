import enum
from typing import Any, Callable, Iterable, NoReturn, TypeAlias
from dataclasses import dataclass

import sys
_MAX_SIZE = sys.maxsize

Square: TypeAlias = tuple[int, int]


class IllegalMoveError(ValueError):
    pass


class Color(enum.IntEnum):
    WHITE = False
    BLACK = True


class Outcome(enum.IntEnum):
    DRAW = -1
    WHITE_WIN = 0
    BLACK_WIN = 1


@dataclass
class CoordinateBounds:
    x: tuple[int | None, int | None] = (None, None)
    y: tuple[int | None, int | None] = (None, None)

    def is_in(self, square: Square) -> bool:
        x, y = square
        (x1, x2), (y1, y2) = self.x, self.y
        for min_bound, t in zip((x1, y1), (x, y)):
            if min_bound is not None and t < min_bound:
                return False
        for max_bound, t in zip((x2, y2), (x, y)):
            if max_bound is not None and t > max_bound:
                return False
        return True


class Board:
    def __init__(self, bounds: CoordinateBounds | None = None) -> None:
        self.squares: dict[Color, set[Square]] = {
            Color.WHITE: set(),
            Color.BLACK: set(),
        }
        if bounds is None:
            self.bounds = CoordinateBounds()
        else:
            self.bounds = bounds

    @property
    def all_squares(self):
        return self.squares[Color.WHITE] | self.squares[Color.BLACK]

    def place(self, square: Square, color: Color) -> None:
        self.squares[color].add(square)

    def remove(self, square: Square, color: Color) -> None:
        self.squares[color].remove(square)

    def clear(self) -> None:
        self.squares = {Color.WHITE: set(), Color.BLACK: set()}

    def is_occupied(self, square: Square, color: Color) -> bool:
        return square in self.squares[color]

    def is_empty_square(self, square: Square) -> bool:
        if not self.bounds.is_in(square):
            return False
        if square in self.all_squares:
            return False
        return True

    def is_empty(self) -> bool:
        return not bool(self.all_squares)

    def is_filled(self) -> bool:
        x, y = self.bounds.x, self.bounds.y
        if None in x + y:
            return False
        if len(self.all_squares) < abs(x[0] - x[1]) * abs(y[0] - y[1]):  # type: ignore
            return False
        return True

    def color_at(self, square: Square) -> Color | None:
        if square in self.squares[Color.WHITE]:
            return Color.WHITE
        if square in self.squares[Color.BLACK]:
            return Color.BLACK
        return None

    def __str__(self) -> str:
        builder = []
        xmin = min(square[0] for square in self.all_squares)
        ymin = min(square[1] for square in self.all_squares)
        xmax = max(square[0] for square in self.all_squares)
        ymax = max(square[1] for square in self.all_squares)
        for y in range(ymax, ymin - 1, -1):
            for x in range(xmin, xmax + 1):
                if (x, y) in self.squares[Color.WHITE]:
                    builder.append("W")
                elif (x, y) in self.squares[Color.BLACK]:
                    builder.append("B")
                else:
                    builder.append(".")
                if x == xmax:
                    builder.append("\n")
        return "".join(builder)


class Gomoku:
    _partial_directions = (
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1),
        (0, 1),
        (1, 0),
        (0, -1),
        (-1, 0),
    )
    _directions = ((1, 1), (0, 1), (1, 0))

    def __init__(self, k: int = 3, bounds: CoordinateBounds | None = None) -> None:
        self._k: int = k
        self.board = Board(bounds=bounds)
        self.turn = Color.WHITE
        self.fullmoves = 0
        self.history: list[tuple[Square, Color]] = []

    def _lines_intersecting_at(
        self, square: Square, color: Color
    ) -> list[list[Square]]:
        lines: list[list[Square]] = []
        x, y = square
        for dir_x, dir_y in self._directions:
            line: list[Square] = []
            if (x, y) in self.board.squares[color]:
                line.append((0, 0))
            for sign in (-1, 1):
                for i in range(1, _MAX_SIZE):
                    if (
                        sq := (x + dir_x * i * sign, y + dir_y * i * sign)
                    ) in self.board.squares[color]:
                        line.append(sq)
                    else:
                        break
            lines.append(line)
        return lines

    def _is_winned_by_connect_at(self, square: Square, color: Color) -> bool:
        for line in self._lines_intersecting_at(square, color):
            if len(line) >= self._k:
                return True
        return False

    def make_move(
        self, move: Square, color: Color | None = None, changeturn: bool = True
    ) -> Square | NoReturn:
        if color is None:
            color = self.turn
        if not self.is_legal_move(move):
            raise IllegalMoveError()
        if changeturn:
            self.turn = Color(not self.turn)
        self.fullmoves += self.turn
        self.history.append((move, color))
        self.board.squares[color].add(move)
        return move

    def is_legal_move(self, move: Square) -> bool:
        return self.board.is_empty_square(move)

    def pop(self) -> tuple[Square, Color] | NoReturn:
        if not self.history:
            raise IndexError("No moves to pop")
        p = self.history.pop()
        self.board.squares[Color(p[1])].remove(p[0])
        return p

    def get_winner_by_connect(self) -> Color | None:
        for square in self.board.all_squares:
            for color in (Color.WHITE, Color.BLACK):
                if self._is_winned_by_connect_at(square, color):
                    return color
        return None

    def get_result(self) -> Outcome | None:
        if (w := self.get_winner_by_connect()) is not None:
            return Outcome(w)
        if self.board.is_filled():
            return Outcome.DRAW
        return None

    def __str__(self) -> str:
        return str(self.board)


class Pente(Gomoku):
    def __init__(
        self,
        maxcaptures: int = 10,
        capturelen: int = 3,
        k: int = 5,
        bounds: CoordinateBounds | None = None,
    ) -> None:
        super().__init__(k, bounds)
        self._maxcaptures: int = maxcaptures
        self._capturelen: int = capturelen
        self._capturecount: list[int] = [0, 0]

    def make_captures_at(self, square: Square) -> list[Square]:
        x, y = square
        color = self.board.color_at(square)
        opposite = Color(not color)
        captures: list[Square] = []
        if color is None:
            return []
        for dir_x, dir_y in self._partial_directions:
            if (
                x + self._capturelen * dir_x,
                y + self._capturelen * dir_y,
            ) not in self.board.squares[color]:
                continue
            if all(
                (x + k * dir_x, y + k * dir_y) in self.board.squares[opposite]
                for k in range(1, self._capturelen)
            ):
                for k in range(1, self._capturelen):
                    square = (x + k * dir_x, y + k * dir_y)
                    self.board.remove(square, opposite)
                    captures.append(square)
        self._capturecount[color] += len(captures)
        return captures

    def get_winner_by_captures(self) -> Color | None:
        if self._capturecount[Color.WHITE] >= self._maxcaptures:
            return Color.WHITE
        if self._capturecount[Color.BLACK] >= self._maxcaptures:
            return Color.BLACK
        return None

    def get_result(self) -> Outcome | None:
        if (w := self.get_winner_by_captures()) is not None:
            return Outcome(w)
        return super().get_result()

    def clear(self) -> None:
        self.board.clear()
        self.turn = Color.WHITE
        self.fullmoves = 0
        self.history: list[tuple[Square, Color]] = []
        self._capturecount = [0, 0]

    def pop(self) -> tuple[Square, Color] | NoReturn:
        last = self.history.pop()
        history = self.history.copy()
        self.clear()
        for move in history:
            self.make_move(*move)
        return last


class Connect6(Gomoku):
    def __init__(self, k: int = 6, bounds: CoordinateBounds | None = None) -> None:
        super().__init__(k, bounds)

    def make_multimove(
        self, *moves: Square, color: Color | None = None, changeturn: bool = True
    ) -> Iterable[Square]:
        if color is None:
            color = self.turn
        for move in moves:
            if not self.is_legal_move(move):
                raise IllegalMoveError()
            self.board.squares[color].add(move)
            self.history.append((move, color))
        if changeturn:
            self.turn = Color(not self.turn)
        self.fullmoves += self.turn
        self.history.append((move, color))
        return moves


class Reversi:
    ...
