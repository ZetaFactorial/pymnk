import unittest
import itertools

from pymnk.mnk import *

class TestTTT(unittest.TestCase):
    def test_finite_dimensions(self):
        for (m,n,k) in itertools.product(range(1,6), repeat=3):
            g = TicTacToe(m,n,k)
            for (i,j) in itertools.product(range(n), range(m)):
                g[i,j] = Piece.X
            g[0,0] = Piece.O
            self.assertEqual(g._flat(), [Piece.O]+[Piece.X]*(m*n-1))

    def test_infinite_dimensions(self):
        g = TicTacToe(m=1, n=1, infinite=True)
        for (i,j) in itertools.product(range(20), range(20)):
            g[i,j] = Piece.X
        self.assertCountEqual(g._flat(), [Piece.X]*(400))

    def test_lines(self):
        X = Piece.X
        O = Piece.O
        g = TicTacToe(m=3, n=2)
        g[0,0], g[1,2], g[0,1], g[0,2], g[1,0], g[1,1] = X, X, O, O, O, O
        lines = [X, O, O], [O, O, X], [X, O], [O, O], [O, X], [X], [O, O], [O, O], [X], [O], [X, O], [O, X], [O]
        self.assertCountEqual(g._lines(), lines)

    def test_fen(self):
        b1 = TicTacToe(3, 3); b1.move(0,1); b1.move(2,0)
        b2 = TicTacToe.from_fen("1X1/3/O2 X 2")
        self.assertEqual(b1.board, b2.board)
        self.assertEqual(b2.turn, Piece.X)
        self.assertEqual(b2.fullmove_number, 2)
        self.assertEqual(b2.fen, "1X1/3/O2 X 2")
        b3 = TicTacToe.from_fen("3 X 1")
        self.assertEqual(b3.m, 3)
        self.assertEqual(b3.n, 1)

    def test_result(self):
        g = TicTacToe()
        self.assertEqual(g.result(), Result.NOTENDED)
        self.assertEqual(g.get_winner(), None)
        g = TicTacToe.from_fen("XXX/OO1/3 O 1")
        self.assertEqual(g.result(), Result.WIN)
        self.assertEqual(g.get_winner(), Piece.X)
        g = TicTacToe.from_fen("OOO/XX1/X2 X 1")
        self.assertEqual(g.result(), Result.WIN)
        self.assertEqual(g.get_winner(), Piece.O)
        g = TicTacToe.from_fen("XOX/OOX/XXO X 1")
        self.assertEqual(g.result(), Result.DRAW)
        self.assertEqual(g.get_winner(), None)

    def test_move(self):
        g = TicTacToe()
        for move in [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2)]:
            g.move(*move)
        g.move(2,0)
        self.assertEqual(g.result(), Result.WIN)
        g.pop()
        self.assertEqual(g.result(), Result.NOTENDED)
        self.assertEqual(g.fen, "XOX/OXO/3 X 4")

    def test_counters(self):
        g = TicTacToe.from_fen("XO1/3/3 X 2")
        self.assertEqual(g.move_count, 0)
        self.assertEqual(g.fullmove_number, 2)

        g.move(2,2)
        self.assertEqual(g.move_count, 1)
        self.assertEqual(g.fullmove_number, 2)

        g.move(2,0)
        self.assertEqual(g.move_count, 2)
        self.assertEqual(g.fullmove_number, 3)

        g.pop()
        self.assertEqual(g.move_count, 1)
        self.assertEqual(g.fullmove_number, 2)

        g.pop()
        self.assertEqual(g.move_count, 0)
        self.assertEqual(g.fullmove_number, 2)

class TestConnect6(unittest.TestCase):
    def test_move_seq(self):
        g = Connect6(m=5,n=5,k=5,p=3,q=2)
        g.move_sequence([(0,1), (0,2)])
        self.assertEqual(g.fen, "1XX2/5/5/5/5 O 1")
        g.move_sequence([(1,1), (1,2), (1,3)])
        self.assertEqual(g.fen, "1XX2/1OOO1/5/5/5 X 2")
        g.move_sequence([(0,0), (0,3), (0,4)])
        self.assertEqual(g.fen, "XXXXX/1OOO1/5/5/5 O 2")

class TestPente(unittest.TestCase):
    def test_pente_capturing(self):
        p = Pente.from_fen("XO2 X 2")
        p.move(0,3)
        self.assertEqual(p.fen, "XO1X O 2")

        p = Pente.from_fen("X1O1 X 2")
        p.move(0,3)
        self.assertEqual(p.fen, "X1OX O 2")

        p = Pente.from_fen("XOV1 X 2")
        p.move(0,3)
        self.assertEqual(p.fen, "X2X O 2")

class TestWildImpartialMisereOrdnchaos(unittest.TestCase):
    def test_moves_and_result(self):
        wild = WildTicTacToe(2,2,2)
        imp = ImpartialTicTacToe(2,2,2)
        mis = MisereTicTacToe(2,2,2)
        oac = OrderAndChaos(2,2,2)
        wild.wild_move(0,0,Piece.O)
        imp.move(0,0)
        mis.move(0,0)
        oac.wild_move(0,0,Piece.X)
        self.assertEqual(wild.fen, "O1/2 O 1")
        self.assertEqual(imp.fen, "X1/2 O 1")
        self.assertEqual(mis.fen, "X1/2 O 1")
        wild.wild_move(0,1,Piece.O)
        imp.move(0,1)
        mis.move(1,0)
        mis.move(0,1)
        oac.wild_move(0,1,Piece.X)
        self.assertEqual(wild.fen, "OO/2 X 2")
        self.assertEqual(imp.fen, "XX/2 X 2")
        self.assertEqual(mis.fen, "XX/O1 O 2")
        self.assertEqual(oac.fen, "XX/2 X 2")
        self.assertEqual(wild.get_winner(), 2)
        self.assertEqual(imp.get_winner(), 2)
        self.assertEqual(mis.get_winner(), 2)
        self.assertEqual(oac.get_winner(), 1)


if __name__ == "__main__":
    unittest.main()