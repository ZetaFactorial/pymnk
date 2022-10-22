# pymnk
## Introduction
Pymnk is a Python library for k-in-a-row games: Gomoku, Pente and Connect6.

## Installing
Install the latest release using pip
```
pip install pymnk
```

## Usage

Initialize game instances
```python
>>> from pymnk import Gomoku, Pente, Connect6
>>> from pymnk import CoordinateBounds
>>> g = Gomoku(bounds=CoordinateBounds((1,19), (1,19)), k=5)
>>> p = Pente(bounds=CoordinateBounds((1,19), (1,19)), k=5, maxcaptures=10, capturelen=3)
>>> c = Connect6(bounds=CoordinateBounds((1,19), (1,19)), k=5)
```

Verify and make moves, revert moves
```python
>>> g.is_legal_move((-3, 6))
False
>>> g.make_move((1,1))
(1, 1)
>>> g.pop()
((1, 1), <Color.WHITE: 0>)
```

Method `make_move` also takes additional parameters `color` and `changeturn`
```python
>>> from pymnk import Color
>>> g = Gomoku()
>>> g.make_move(move=(1,2), color=Color.BLACK, changeturn=False)
(1, 2)
>>> g.turn
<Color.WHITE: 0>
>>> g.history
[((1, 2), <Color.BLACK: 1>)]
```


Class `CoordinateBounds` restricts `x` and `y` coordinates on the rectangular board. You can assigning a bound to `None` to make a coordinate unbounded
```python
>>> g = Gomoku(bounds=CoordinateBounds((1, None), (None, 25)))
>>> g.make_move((2000, -100))
(2000, -100)
```
Parameter `bounds` may be omitted. That would make the board unbounded
```python
>>> g = Gomoku()
>>> g.make_move((1000000, -9999999999))
(1000000, -9999999999)
```

Get the result of a game
```python
>>> g = Gomoku(bounds=CoordinateBounds((1,19), (1,19)), k=2)
>>> g.make_move((1,1))
(1, 1)
>>> g.make_move((1,2))
(1, 2)
>>> g.make_move((2,2))
(2, 2)
>>> g.get_winner_by_connect()
<Color.WHITE: 0>
>>> g.get_result()
<Outcome.WHITE_WIN: 0>
```

Class `Pente` is inherited from `Gomoku` and simply allows you to perform custodial captures
```python
>>> g = Pente(k=5, maxcaptures=2, bounds=CoordinateBounds((1,13), (1,13)))
>>> g.make_move((1,1))
(1, 1)
>>> g.make_move((2,2))
(2, 2)
>>> g.make_move((5,10))
(5, 10)
>>> g.make_move((3,3))
(3, 3)
>>> g.make_move((4,4))
(4, 4)
>>> g.make_captures_at((4,4))
[(3, 3), (2, 2)]
>>> g.get_winner_by_captures()
<Color.WHITE: 0>
```

Class `Connect6` also inherits from `Gomoku` and allows you to make more than one move at a time
```python
>>> c = Connect6(k=6, bounds=CoordinateBounds((1,19), (1,19)))
>>> c.make_multimove((1,1), (3,3))
((1, 1), (3, 3))
```

Show a simple ASCII representation of the board
```python
>>> g = Connect6()
>>> g.make_multimove((1,1), (2,5), (-1,3))
((1, 1), (2, 5), (-1, 3))
>>> g.make_multimove((1,4), (5,3), (-1,2))
((1, 4), (5, 3), (-1, 2))
>>> print(g)
...W...
..B....
W.....B
B......
..W....
```

## License

Pymnk is available under the MIT license. For the full text, check out `LICENSE`.