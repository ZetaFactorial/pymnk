# from __future__ import annotations

# import random
# import math

# from pymnk.mnk import *

# MAX_EVAL = 100

# # The problem is that some child classes of MNK() define their own
# # methods for moving and move generation.
# def mnk_legal_moves(game: MNKType) -> Iterator:
#     if type(game) is Connect6:
#         return game.legal_move_sequences()
#     if type(game) is WildTicTacToe or type(game) is OrderAndChaos:
#         return game.legal_wild_moves()
#     elif hasattr(game, "legal_moves"):
#         return game.legal_moves()
#     else:
#         raise TypeError("Invalid game type")

# def mnk_move(game: MNKType, move) -> None:
#     if type(game) is Connect6:
#         game.move_sequence(move)
#     elif type(game) is WildTicTacToe or type(game) is OrderAndChaos:
#         game.wild_move(*move)
#     elif hasattr(game, "legal_moves"):
#         game.move(*move)
#     else:
#         raise TypeError("Invalid game type")

# class Engine:
#     @staticmethod
#     def minimax_evaluate(game: MNKType, maximizing: bool = True, depth: int = 3) -> int:
#         res = game.result()
#         if not depth:
#             if res == Result.WIN:
#                 return +MAX_EVAL if game.get_winner() == Piece.X else -MAX_EVAL
#             elif res == Result.DRAW:
#                 return 0
#             return 0

#         if maximizing:
#             value = -MAX_EVAL
#             for move in mnk_legal_moves(game):
#                 mnk_move(game, move)
#                 value = max(value, Engine.minimax_evaluate(game, False, depth-1))
#                 game.pop()
#             return value

#         else:
#             value = +MAX_EVAL
#             for move in mnk_legal_moves(game):
#                 mnk_move(game, move)
#                 value = min(value, Engine.minimax_evaluate(game, True, depth-1))
#                 game.pop()
#             return value

#     @staticmethod
#     def minimax_response(game: MNKType, depth=3):
#         best_evaluation = -MAX_EVAL if game.turn == Piece.X else MAX_EVAL
#         best_move = None
#         sgn = int(math.copysign(1, best_evaluation))
#         for move in mnk_legal_moves(game):
#             mnk_move(game, move)
#             if (ev := Engine.minimax_evaluate(game, depth)*sgn) >= best_evaluation*sgn or best_move is None:
#                 best_evaluation = ev
#                 best_move = move
#             game.pop()
#         return best_move

#     @staticmethod
#     def random_response(game):
#         return random.choice(list(mnk_legal_moves(game)))