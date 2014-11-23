class Human(object):
    """An interface for a human player."""
    
    def __init__(self, t):
        self.t = t
        if t == 'X':
            self.other_t = 'O'
        else:
            self.other_t = 'X'

    def get_move(self, board):
        """Get a move from the player through stdin"""
        success = False
        while not success:
            try:
                move = int(raw_input("[%s] Enter column: " % self.t))
            except ValueError:
                print "Error: column must be an integer."
                continue
            if board.is_playable(move):
                success = True
            else:
                print "Error: invalid move."

        return move, self.t
