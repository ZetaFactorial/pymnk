# from __future__ import annotations

# import re
# import itertools
# import enum

# from typing import Iterator, Optional, TypeVar

# Board = list[list["Piece"]]
# Square = tuple[int, int]
# MNKType = TypeVar('MNKType', bound="TicTacToe")

# PIECE_SYMBOLS: str = ".XOVTZ"
# PIECE_UNICODE_SYMBOLS: str = "🟩⬜⬛🟥🟦🟨"


# class Piece(enum.IntEnum):
#     E, X, O, V, T, Z = range(6)

#     @classmethod
#     def from_symbol(cls, piece: str) -> Piece:
#         return cls(PIECE_SYMBOLS.index(piece))

#     def symbol(self) -> str:
#         return PIECE_SYMBOLS[self]

#     def unicode_symbol(self) -> str:
#         return PIECE_UNICODE_SYMBOLS[self]

#     def nxt(self, players: int) -> Piece:
#         return Piece(self+1) if self < players else Piece(1)

#     def prev(self, players: int) -> Piece:
#         return Piece(self-1) if self > 1 else Piece(players)

#     def __str__(self) -> str:
#         return self.symbol()


# class Result(enum.IntEnum):
#     DRAW = -1
#     NOTENDED = 0
#     WIN = +1


# class TicTacToe:
#     def __init__(self, m: int = 3, n: int = 3, k: int = 3, infinite: bool = False, players: int = 2) -> None:
#         if m <= 0 or n <= 0 or k <= 0:
#             raise ValueError("Parameters m, n, k must be positive.")
        
#         self.m: int = m
#         self.n: int = n
#         self.k: int = k

#         self.board: Board = [[Piece.E]*m for _ in range(n)]

#         self.players: int = players
#         self.turn: Piece = Piece.X
#         self.move_count: int = 0
#         self.fullmove_number: int = 1
#         self.infinite: bool = infinite
#         self.move_history: list[Square] = []

#     @property
#     def fen(self) -> str:
#         """Creates a FEN representation of the game board.

#         A FEN string contains three fields:
#         1. Board representation. Rows are separated by "/" symbol. Pieces are denoted 
#         by its symbols. A line of empty squares is denoted by its length.
#         2. Active player symbol.
#         3. The fullmove number. Starts with 1 and incremented after the last player's move.

#         For example, the starting position of Tic Tac Toe is '3/3/3 X 1'.
#         """
#         fen = "/".join(("".join(map(Piece.symbol, row)) for row in self.board))
#         fen = re.sub(r"\.+", lambda x: str(len(x.group())), fen)
#         fen = " ".join([fen, str(self.turn), str(self.fullmove_number)])
#         return fen

#     @classmethod
#     def from_fen(cls: type[MNKType], fen: str) -> MNKType:
#         """Initializes a class instance from FEN. Does not check if given FEN is valid."""
#         position, turn, fullmove_number = fen.split()

#         position = re.sub(r"[0-9]+", lambda x: "."*int(x.group()), position)
#         position_rows = position.split("/")
#         game = cls(m=len(position_rows[0]), n=len(position_rows))
#         game.board = [list(map(Piece.from_symbol, row)) for row in position_rows]
        
#         game.turn = Piece.from_symbol(turn)
#         game.fullmove_number = int(fullmove_number)
        
#         return game
        
#     def change_turn(self) -> None:
#         self.turn = self.turn.nxt(self.players)

#     def revert_turn(self) -> None:
#         self.turn = self.turn.prev(self.players)

#     def _columns(self) -> list[list[Piece]]:
#         return [list(square) for square in zip(*self.board)]

#     def _diagonals(self) -> list[list[Piece]]:
#         diags: list[list[Piece]] = []
#         for sm in range(self.m+self.n-1):
#             strip: list[Piece] = []
#             for (i, j) in filter(lambda square: sum(square)==sm, self.all_coords()):
#                 strip.append(self[i, j])
#             diags.append(strip)
#         return diags

#     def _antidiagonals(self) -> list[list[Piece]]:
#         rotated_board = TicTacToe(m=self.n, n=self.m)
#         rotated_board.board = list(zip(*self.board))[::-1] # type: ignore
#         # This board is actually invalid. rotated_board.board is list[tuple[..]], not list[list[..]]. But it works.
#         return rotated_board._diagonals()

#     def _lines(self) -> list[list[Piece]]:
#         return self.board + self._columns() + self._diagonals() + self._antidiagonals()

#     def _check_line_winned(self, line: list[Piece]) -> bool:
#         if self.k > len(line):
#             return False
        
#         for i, _ in enumerate(line[:1-self.k]):
#             flag = True
            
#             next_k_squares = line[i:i+self.k]

#             for square in next_k_squares:  
#                 if not square*next_k_squares[0] or square != next_k_squares[0]:
#                     flag = False
#                     continue
            
#             if flag:
#                 return True
        
#         return False

#     def _is_filled(self) -> bool:
#         return Piece.E not in self._flat()

#     def _checkwin(self) -> bool:
#         return any(self._check_line_winned(line) for line in self._lines())

#     def get_winner(self) -> Optional[Piece]:
#         if self.result() == Result.WIN:
#             return self.turn.prev(self.players)
#         return None

#     def result(self) -> Result:
#         if self._checkwin():
#             return Result.WIN
#         elif self._is_filled():
#             return Result.DRAW
#         else:
#             return Result.NOTENDED

#     def is_legal_move(self, x: int, y: int) -> bool:
#         """Checks move legality. Does not check if the game is already over."""
#         try:
#             return self[x, y] == Piece.E
#         except IndexError:
#             return False

#     def move(self, x: int, y: int) -> None:
#         """Places a piece on the given square and changes turn."""
#         if self.is_legal_move(x, y):
#             self.fullmove_number += 1 if self.turn == self.players else 0
#             self[x, y] = self.turn
#             self.move_history.append((x,y))
#             self.move_count += 1
#             self.change_turn()
#         else:
#             raise ValueError("Invalid move")

#     def pop(self) -> None:
#         """Reverts game state to the previous position."""
#         if not self.move_count:
#             raise IndexError("pop game with empty history")

#         last_move = self.move_history[-1]

#         self.move_count -= 1
#         self.fullmove_number -= 1 if self.turn == Piece.X else 0
#         self.move_history.pop()
#         self[last_move[0], last_move[1]] = Piece.E
#         self.revert_turn()

#     def reset(self) -> None:
#         """Reverts game to the original position."""
#         self.board = [[Piece.E]*self.m for _ in range(self.n)]
#         self.turn = Piece.X
#         self.move_count = 0
#         self.fullmove_number = 1
#         self.move_history = []

#     def legal_moves(self) -> Iterator[Square]:
#         return (square for square in self.all_coords() if self.is_legal_move(*square))
    
#     def _flat(self) -> list[Piece]:
#         return sum(self.board, [])

#     def all_coords(self) -> Iterator[Square]:
#         return (square for square in itertools.product(range(self.n), range(self.m)))

#     def _increase_dimensions(self, to_dim: int) -> None:
#         assert self.infinite
#         newboard = [[Piece.E]*to_dim for _ in range(to_dim)]

#         for (x, y) in itertools.product(range(to_dim), repeat=2):
#             newboard[x][y] = self[x, y] if (x, y) in self.all_coords() else Piece.E

#         self.n, self.m = to_dim, to_dim
#         self.board = newboard.copy()

#     def __getitem__(self, key: Square) -> Piece:
#         if not key in self.all_coords() and not self.infinite:
#             raise IndexError("Board index out of range.")

#         if not key in self.all_coords() and self.infinite:
#             to_dim = max(key[0]+1, key[1]+1)
#             self._increase_dimensions(to_dim)

#         return self.board[key[0]][key[1]]

#     def __setitem__(self, key: Square, value: Piece) -> None:
#         if not key in self.all_coords() and not self.infinite:
#             raise IndexError("Board index out of range.")

#         if not key in self.all_coords() and self.infinite:
#             to_dim = max(key[0]+1, key[1]+1)
#             self._increase_dimensions(to_dim)
  
#         self.board[key[0]][key[1]] = value

#     def unicode(self) -> str:
#         builder = []
#         for row in self.board:
#             for piece in row:
#                 builder.append(Piece.unicode_symbol(piece))
#             builder.append("\n")
#         return "".join(builder)

#     def __repr__(self) -> str:
#         return f"{type(self).__name__}.from_fen('{self.fen}')"

#     def __str__(self) -> str:
#         builder = []
#         for row in self.board:
#             for piece in row:
#                 builder.append(Piece.symbol(piece))
#             builder.append("\n")
#         return "".join(builder)

#     def _game_attributes(self):
#         attrs = []
#         for key, value in self.__dict__.items():
#            attrs.append(f"{key}: {value!r}\n")
#         return "".join(attrs)


# class Connect6(TicTacToe):
#     def __init__(self, m: int = 19, n: int = 19, k: int = 6, p: int = 2, q: int = 1, infinite: bool = False) -> None:
#         super().__init__(m, n, k, infinite, players=2)
#         self.p: int = p
#         self.q: int = q
#         assert q <= m*n


#     def current_move_sequence_len(self) -> int:
#         """Determines what move sequence length must be played on the current turn."""
#         empty_squares: int = self.m*self.n - self.move_count
#         if not self.move_count:
#             return self.q
#         elif empty_squares < self.p:
#             return empty_squares
#         else:
#             return self.p

#     def is_legal_move_sequence(self, moves: list[Square]) -> bool:
#         return self.current_move_sequence_len() == len(moves) and all(self.is_legal_move(*move) for move in moves)

#     def move_sequence(self, moves: list[Square]) -> None:
#         """Makes Connect6 move, changes turn."""
#         if self.is_legal_move_sequence(moves):
#             self.fullmove_number += 1 if self.turn == self.players else 0

#             for move in moves:
#                 self[move[0], move[1]] = self.turn
                
#                 self.move_history.append(move)
#                 self.move_count += 1

#             self.change_turn()
#         else:
#             raise ValueError("Invalid move")

#     def legal_move_sequences(self) -> Iterator[list[Square]]:
#         """Returns Connect6 legal moves."""
#         seq_len = self.current_move_sequence_len()
#         return (list(seq) for seq in itertools.combinations(self.legal_moves(), r=seq_len))

#     def pop(self) -> None:
#         """Reverts game state to the previous position (before the last move sequence)."""
#         if not self.move_count:
#             raise IndexError("pop game with empty history")

#         self.move_count -= self.p
#         self.fullmove_number -= 1 if self.turn == self.players else 0
        
#         for _ in range(self.p):
#             if not self.move_history:
#                 break
#             last_move = self.move_history[-1]
#             self.move_history.pop()
#             self[last_move[0], last_move[1]] = Piece.E

#         self.revert_turn()


# class Pente(TicTacToe):
#     def __init__(self, m: int = 3, n: int = 3, k: int = 3, infinite: bool = False, players: int = 2) -> None:
#         super().__init__(m, n, k, infinite, players)
#         self.capture_count: list[int] = [0]*players
#         self.captures_to_win: int = 10
#         self.capture_history: list[list[Square]] = []

#     def custodial_capture(self, x: int, y: int, length: int) -> int:
#         """Makes all custodial captures on the position and returns how much pieces were captured."""
#         capture_count = 0

#         self.capture_history.append([])
#         last_captures = self.capture_history[-1]

#         for dir_x, dir_y in itertools.product((-1, 0, 1), repeat=2):
#             if dir_x == 0 and dir_y == 0:
#                 continue

#             try:
#                 if self[x, y] != self[x+(length+1)*dir_x, y+(length+1)*dir_y]:
#                     continue
#             except IndexError:
#                 continue
            
#             if all(self[x+i*dir_x, y+i*dir_y] not in (self[x, y], Piece.E) for i in range(1, length+1)):  
#                 for i in range(1, length+1):
#                     self[x+i*dir_x, y+i*dir_y] = Piece.E
#                     last_captures.append((x+i*dir_x, y+i*dir_y))

#             capture_count += length

#         return capture_count

#     def _checkwin(self) -> bool:
#         return super()._checkwin() or max(self.capture_count) >= self.captures_to_win

#     def move(self, x: int, y: int) -> None:
#         """Places a piece on the given square, makes custodial captures and changes turn."""
#         super().move(x, y)
#         self.capture_count[self.turn-1] += self.custodial_capture(x, y, 2)

#     def pop(self) -> None:
#         super().pop()
#         for (i,j) in self.capture_history[-1]:
#             self[i,j] = Piece.E
#         self.capture_history.pop()

#     def reset(self) -> None:
#         super().reset()
#         self.capture_count = [0]*self.players
#         self.capture_history = []


# class UltimateTicTacToe(TicTacToe):
#     def __init__(self, m: int = 3, n: int = 3, k: int = 3, which_local_board: Square = (0, 0), players: int = 2) -> None:
#         super().__init__(m, n, k, False, players)
#         # Global board (self.board) contain winners of corresponding local boards.
#         self.localboards: list[list[TicTacToe]] = [[TicTacToe(m, n, k, False, players) for _ in range(m)] for _ in range(n)]
#         self.which_local_board: Square = which_local_board
#         self.which_local_board_history: list[Square] = [which_local_board]

#     def is_legal_move(self, x: int, y: int) -> bool:
#         """Checks move legality. Note that we can move on an already winned local board."""
#         return self.localboards[self.which_local_board[0]][self.which_local_board[1]].is_legal_move(x, y)

#     def move(self, x: int, y: int) -> None:
#         if self.is_legal_move(x, y):
#             self.fullmove_number += 1 if self.turn == self.players else 0

#             localboard = self.localboards[self.which_local_board[0]][self.which_local_board[1]]
#             localboard[x, y] = self.turn
#             localboard.move_history.append((x,y))

#             self.move_history.append((x,y))
#             self.move_count += 1
            
#             self.which_local_board = (x, y)
#             self.which_local_board_history.append(self.which_local_board)

#             localwinner =  localboard.result()
#             if localwinner is not None:
#                 self.board[x][y] = Piece(localwinner)

#             self.change_turn()
#         else:
#             raise ValueError("Invalid move")

#     def pop(self) -> None:
#         if not self.move_count:
#             raise IndexError("pop game with empty history")

#         self.which_local_board_history.pop()
#         self.which_local_board = self.which_local_board_history[-1]
        
#         localboard = self.localboards[self.which_local_board[0]][self.which_local_board[1]]
#         localboard.pop()

#         last_move = self.move_history[-1]

#         self.move_count -= 1
#         self.fullmove_number -= 1 if self.turn == 1 else 0
#         self.move_history.pop()

#         localwinner =  localboard.get_winner()
#         if localwinner is not None:
#             self[last_move[0], last_move[1]] = localwinner
        
#         self.revert_turn()

#     def reset(self) -> None:
#         super().reset()
#         self.localboards = [[TicTacToe(self.m, self.n, self.k, False, self.players) for _ in range(self.m)] for _ in range(self.n)]
#         self.which_local_board = self.which_local_board_history[0]
#         self.which_local_board_history = [self.which_local_board]

#     def fen(self) -> str:
#         """TODO"""

#     @classmethod
#     def from_fen(cls: type[MNKType], fen: str) -> MNKType:
#         """TODO"""


# class MisereTicTacToe(TicTacToe):
#     def __init__(self, m=3, n=3, k=3, infinite=False, players: int = 2) -> None:
#         super().__init__(m, n, k, infinite, players)
    
#     def get_winner(self) -> Optional[Piece]:
#         if (reg_winner := super().get_winner()) is not None:
#             return reg_winner.prev(self.players)
#         return None


# class WildTicTacToe(TicTacToe):
#     def __init__(self, m=3, n=3, k=3, infinite=False, players: int = 2) -> None:
#         super().__init__(m, n, k, infinite, players)
#         self.move_history_pieces: list[Piece] = [] # Which pieces were chosen on each move

#     def wild_move(self, x: int, y: int, piece: Piece) -> None:
#         """Wild analogue of move, giving the option of choosing piece to place."""
#         if self.is_legal_move(x, y):
#             self.fullmove_number += 1 if self.turn == self.players else 0
#             self[x, y] = piece
#             self.move_history.append((x,y))
#             self.move_history_pieces.append(piece)
#             self.move_count += 1
#             self.change_turn()
#         else:
#             raise ValueError("Invalid move")
    
#     def legal_wild_moves(self) -> Iterator[tuple[int, int, Piece]]:
#         return ((x, y, piece) for piece in map(Piece, range(1, self.players+1)) for (x, y) in self.legal_moves())

#     def pop(self) -> None:
#         super().pop()
#         self.move_history_pieces.pop()


# class ImpartialTicTacToe(WildTicTacToe):
#     def __init__(self, m=3, n=3, k=3, infinite=False, players: int = 2) -> None:
#         super().__init__(m, n, k, infinite, players)

#     def move(self, x: int, y: int) -> None:
#         super().wild_move(x, y, Piece.X)


# class OrderAndChaos(WildTicTacToe):
#     def __init__(self, m=3, n=3, k=3, infinite=False) -> None:
#         super().__init__(m, n, k, infinite, players=2)

#     def get_winner(self) -> Optional[Piece]:
#         """'X' is Chaos, 'O' is Order."""
#         if res := self.result():
#             return Piece.X if res == Result.WIN else Piece.O
#         return None

#     def result(self) -> Result:
#         if super().result() in (Result.WIN, Result.DRAW):
#             return Result.WIN
#         return Result.NOTENDED