import sys

from connector.board import Board
from connector.human import Human
from connector.ai import AI


def make_player(p_type, marker):
    if p_type[0] == 'h':
        player = Human(marker)
    else:
        player = AI(marker, 4)
    return player


def usage():
    print "usage: python %s player1 player2 rows cols win-size" % sys.argv[0]
    sys.exit(1) 


if len(sys.argv) != 6:
    usage()

player1, player2 = map(str.lower, sys.argv[1:3])
player_types = ['human', 'ai', 'h', 'a']
if player1 not in player_types or player2 not in player_types:
    usage()

try:
    rows, cols, win_size = map(int, sys.argv[3:])
except ValueError:
    usage()

board = Board((rows, cols), win_size)

players = [make_player(player1, 'X'), make_player(player2, 'O')]
n_players = len(players)
cur_player = 0

board.print_board()
print ""

while board.get_winning_group() is None and not board.is_full():
    col, t = players[cur_player].get_move(board)
    board.drop_piece(col, t)
    board.print_board()
    print "Player %s played at column %s" % (t, col)
    print ""
    cur_player = (cur_player + 1) % n_players

print ""
print "GAME OVER!"

if board.get_winning_group() is not None:
    winner = board[board.get_winning_group()[0]]
    print "Player %s wins!" % winner
else:
    print "It's a tie!"