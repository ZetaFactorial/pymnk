import unittest

from pymnk.mnk import *


class TestCoordinateBounds(unittest.TestCase):
    def test_basic(self):
        cb = CoordinateBounds((0,5), (-3,0))
        self.assertTrue(cb.is_in((3,-2)))
        self.assertTrue(cb.is_in((0,-2)))
        self.assertFalse(cb.is_in((3,-200)))
        self.assertFalse(cb.is_in((100,-2)))
        self.assertFalse(cb.is_in((100,-200)))
        cb2 = CoordinateBounds((0,None), (None,0))
        self.assertTrue(cb2.is_in((5,-10)))
        self.assertFalse(cb2.is_in((-5,0)))


class TestBoard(unittest.TestCase):
    def test_basic(self):
        b = Board(CoordinateBounds((0,3), (0,3)))
        b.place(Square((0,1)), Color.WHITE)
        b.place(Square((1,1)), Color.BLACK)
        self.assertEqual(b.squares, {Color.WHITE: {(0,1)}, Color.BLACK: {(1,1)}})
        self.assertTrue(b.is_occupied((1,1), Color.BLACK))
        self.assertFalse(b.is_empty())
        self.assertTrue(b.is_empty_square(Square((2,3))))
    def test_str(self):
        b = Board(CoordinateBounds((1,3), (1,None)))
        b.place(Square((2,1)), Color.BLACK)
        b.place(Square((3,1)), Color.WHITE)
        b.place(Square((2,2)), Color.BLACK)
        b.place(Square((1,3)), Color.WHITE)
        self.assertEqual(str(b), '''W..\n.B.\n.BW\n''')

        
class TestGomoku(unittest.TestCase):
    def test_move(self):
        g = Gomoku(k=3, bounds=CoordinateBounds((1,3), (1,3)))
        g.make_move(Square((2,2)))
        self.assertEqual(g.board.squares, {Color.WHITE: {(2,2)}, Color.BLACK: set()})
        g.make_move(Square((2,3)))
        self.assertEqual(g.board.squares, {Color.WHITE: {(2,2)}, Color.BLACK: {(2,3)}})
        self.assertRaises(IllegalMoveError, g.make_move, Square((-100, -100)))
        self.assertRaises(IllegalMoveError, g.make_move, Square((2, 2)))
    
    def test_pop(self):
        g = Gomoku(k=3, bounds=CoordinateBounds((1,3), (1,3)))
        g.make_move(Square((2,2)))
        g.pop()
        self.assertEqual(g.board.squares, {Color.WHITE: set(), Color.BLACK: set()})
    
    def test_win_connect(self):
        g = Gomoku(k=2, bounds=CoordinateBounds((1,3), (1,3)))
        g.make_move(Square((1,1)))
        g.make_move(Square((2,1)))
        g.make_move(Square((1,2)))
        self.assertEqual(g.get_result(), Outcome.WHITE_WIN)
        g = Gomoku(k=2, bounds=CoordinateBounds((1,3), (1,3)))
        
    def test_draw(self):
        g = Gomoku(k=4, bounds=CoordinateBounds((1,2), (1,2)))
        g.make_move(Square((1,1)))
        g.make_move(Square((2,1)))
        g.make_move(Square((1,2)))
        g.make_move(Square((2,2)))
        self.assertEqual(g.get_result(), Outcome.DRAW)
        
class TestPente(unittest.TestCase):
    def test_capture_success(self):
        g = Pente(k=4, maxcaptures=2, bounds=CoordinateBounds((1,10), (1,10)))
        g.make_move(Square((1,1)))
        g.make_move(Square((2,2)))
        g.make_move(Square((10,4)))
        g.make_move(Square((3,3)))
        g.make_move(Square((4,4)))
        g.make_captures_at(Square((4,4)))
        self.assertEqual(g.board.squares, {Color.WHITE: {(1,1), (4,4), (10,4)}, Color.BLACK: set()})

    def test_capture_fail(self):
        g = Pente(k=4, bounds=CoordinateBounds((1,10), (1,10)))
        g.make_move(Square((1,1)))
        g.make_move(Square((2,2)))
        g.make_captures_at(Square((2,2)))
        self.assertEqual(g.board.squares, {Color.WHITE: {(1,1)}, Color.BLACK: {(2,2)}})

    def test_win_captures(self):
        g = Pente(k=4, maxcaptures=2, bounds=CoordinateBounds((1,10), (1,10)))
        g.make_move(Square((1,1)))
        g.make_move(Square((2,2)))
        g.make_move(Square((10,4)))
        g.make_move(Square((3,3)))
        g.make_move(Square((4,4)))
        g.make_captures_at(Square((4,4)))
        self.assertEqual(g.get_winner_by_captures(), Outcome(Color.WHITE))
        self.assertEqual(g.get_result(), Outcome(Color.WHITE))

    def test_pop(self):
        g = Pente(k=3, bounds=CoordinateBounds((1,3), (1,3)))
        g.make_move(Square((2,2)))
        g.pop()
        self.assertEqual(g.board.squares, {Color.WHITE: set(), Color.BLACK: set()})

class TestConnect6(unittest.TestCase):
    def test_capture_success(self):
        g = Connect6(k=4, bounds=CoordinateBounds((1,10), (1,10)))
        g.make_multimove((1,1), (1,2))
        g.make_multimove((1,4))
        self.assertEqual(g.board.squares, {Color.WHITE: {(1,1), (1,2)}, Color.BLACK: {(1,4)}})


if __name__ == "__main__":
    unittest.main()