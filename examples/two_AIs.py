import time
import os

from pymnk.engine import Engine
from pymnk.mnk import TicTacToe

def clear() -> None:
    os.system('cls' if os.name=='nt' else 'clear')

def main() -> None:
    game = TicTacToe(m=5, n=5, k=3, infinite=False, players=2)
    while not game.result():
        resp = Engine.random_response(game)
        clear()
        print(f'Next move is {resp} by {game.turn}:\n')
        game.move(*resp)
        print(game.unicode())
        time.sleep(0.5)
    result = game.result()
    if result:
        print(f'{game.get_winner()} has won!')
    else:
        print(f'It is a draw.')

if __name__ == '__main__':
    main()