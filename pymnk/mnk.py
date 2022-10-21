from abc import ABC, abstractmethod
import enum
from typing import Any, Callable, NoReturn, TypeAlias
from functools import wraps
from dataclasses import dataclass

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
    def __init__(self, bounds: CoordinateBounds | None = None):
        self.squares: dict[Color, set[Square]] = {Color.WHITE: set(), Color.BLACK: set()}
        if bounds is None:
            self.bounds = CoordinateBounds()
        else:
            self.bounds = bounds
    
    def is_occupied(self, square: Square, color: Color) -> bool:
        return square in self.squares[color]
    
    def is_empty_square(self, square: Square) -> bool:
        if not self.bounds.is_in(square):
            return False
        for color in (Color.BLACK, Color.WHITE):
            if square in self.squares[color]:
                return False
        return True
    
    def is_empty(self) -> bool:
        return not any(bool(self.squares[color]) for color in (Color.BLACK, Color.WHITE))


def _wrap_move(movemaker: Callable) -> Callable:
    @wraps(movemaker)
    def wrapped(self, move: Square) -> Square | NoReturn:
        if not self.is_legal_move(move):
            raise IllegalMoveError()
        self.movemaker(move)
        self.turn = not self.turn
        self.fullmoves += self.turn
        self.history.append(move)
        return move
    return wrapped


class BaseGame(ABC):
    def __init__(self, bounds: CoordinateBounds | None = None, first: Color = Color.WHITE, *args: Any, **kwargs: Any) -> None:
        self.board = Board(bounds=bounds)
        self.turn = first
        self.fullmoves = 0
        self.history: list[Square] = []

    @_wrap_move
    @abstractmethod
    def make_move(self, move: Square) -> Square | None:
        ...
        
    @abstractmethod
    def is_legal_move(self, move: Square) -> bool:
        ...
    
    @abstractmethod
    def pop(self) -> Square | None:
        ...
        
    @abstractmethod
    def get_result(self) -> Outcome | None:
        ...


class TTT(BaseGame):
    _partial_directions = ((1,1), (1,-1), (-1, 1), (-1,-1), (0,1), (1,0), (0,-1), (-1,0))
    _directions = ((1,1), (0,1), (1,0))
    
    def __init__(self, k: int = 3, bounds: CoordinateBounds | None = None, first: Color = Color.WHITE, *args: Any, **kwargs: Any) -> None:
        super().__init__(bounds, first, *args, **kwargs)
        self.k = k
    
    def lines_intersecting_at(self, square: Square, color: Color) -> list[list[Square]]:
        lines: list[list[Square]] = []
        x, y = square
        for dir_x, dir_y in self._directions:
            line: list[Square] = []
            for sign in (-1,1):
                k = 0
                while 1:
                    k += 1
                    if (sq := Square((x+dir_x*k*sign, y+dir_y*k*sign))) not in self.board.squares[color]: # type: ignore
                        break
                    else:
                        line.append(sq)
            lines.append(line)
        return lines

    def _check_winned(self, k: int, lines: list[list[Square]]) -> bool:
        for line in lines:
            if len(line) >= k:
                return True
        return False
         
    @_wrap_move
    def make_move(self, move: Square) -> Square | NoReturn:
        self.board.squares[self.turn].add(move)
        return move
        
    def is_legal_move(self, move: Square) -> bool:
        return self.board.is_empty_square(move)
    
    def pop(self) -> Square | None:
        self.board.squares[Color(not self.turn)].remove(p := self.history.pop())
        return p        
    
    def get_result(self) -> Outcome | None:
        if self._check_winned(self.k, self.lines_intersecting_at(self.board.squares[Color(not self.turn)], )):
            return Outcome(not self.turn)
        ...